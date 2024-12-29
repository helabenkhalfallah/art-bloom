import numpy
import pandas
from tortoise.transactions import in_transaction

from artworks_core.artworks_data_helper import format_artworks_by_params
from artworks_core.models import Artwork
from artworks_settings import get_app_instance
from artworks_utils import logger, handle_get_request

user_preferences = {
    "style_title": "Post-Impressionism",
    "medium_display": "Oil on canvas",
    "category_titles": ["Painting and Sculpture of Europe"]
}

async def get_total_artworks():
    """
    Fetches the total number of artworks from the external API.

    Returns:
        int: Total number of artworks, or 0 if the count is unavailable.
    """
    response = await handle_get_request(get_app_instance().config.ARTWORKS_API, {})

    try:
        return response["data"]["pagination"]["total"]
    except KeyError as exception:
        logger.info("get_total_artworks exception: %s", exception)
        return 0

async def get_or_create_artwork(**kwargs):
    """
    Gets an artwork if it exists, otherwise creates it.

    Args:
        **kwargs: Fields to match or create the artwork.

    Returns:
        tuple: (artwork, created) where `artwork` is the instance and `created` is a boolean.
    """
    try:
        # Check if an artwork already exists
        artwork = await Artwork.get_or_none(**kwargs)
        if artwork:
            return artwork, False
        # Otherwise, create a new instance
        artwork = await Artwork.create(**kwargs)
        return artwork, True
    except Exception as exception:
        logger.error("Error in get_or_create_artwork: %s", exception)
        raise

async def get_artworks_by_params(params):
    """
    Fetches artworks based on pagination and sorting parameters.

    Args:
        params (dict): Query parameters containing pagination and sorting information.

    Returns:
        dict: Serialized and formatted list of artworks with HTTP status code.
    """
    try:
        try:
            page = int(params['page'][0])  # Use a string default to align with list
            limit = int(params['limit'][0])  # Use a string default
        except (ValueError, IndexError) as exception:
            logger.error("Invalid pagination parameters: %s", exception)
            page, limit = 1, 10

        logger.debug("get_artworks_by_params page: %s, limit: %s", page, limit)

        # Calculate the offset
        offset = (page - 1) * limit

        # Fetch paginated data
        artworks = await Artwork.all().offset(offset).limit(limit)

        # Serialize data
        serialized_artworks = [artwork.to_dict() for artwork in artworks]
        data_by_params = await format_artworks_by_params(serialized_artworks, params)

        return {"data": data_by_params, "status": 200}
    except Exception as exception:
        logger.error("get_artworks_by_params exception: %s", exception)
        return {"data": [], "status": 400}

async def get_artwork_by_id(artwork_id):
    """
    Retrieves a single artwork's data based on its ID.

    Args:
        artwork_id (str): The ID of the artwork to retrieve.

    Returns:
        dict: A dictionary containing the artwork data and a status code.
            - "data": The serialized artwork data or an empty list if not found.
            - "status": HTTP status code (200 for success, 400 for errors).

    Logs:
        Logs the artwork ID being queried and any exceptions encountered.

    Example: >>> await get_artwork_by_id("123")
        {"data": {"id": "123", "title": "Mona Lisa"}, "status": 200}
    """
    logger.info("get_artwork_by_id artwork_id: %s", artwork_id)
    try:
        # Find artwork by id
        artwork = await Artwork.get_or_none(id=artwork_id)

        # Serialize data
        serialized_artwork = artwork.to_dict()

        return {"data": serialized_artwork, "status": 200}
    except Exception as exception:
        logger.error("get_artwork_by_id exception: %s", exception)
        return {"data": [], "status": 400}

async def search_artworks(params):
    """
    Searches for artworks based on query parameters by querying an external API.

    Args:
        params (dict): Query parameters containing the search criteria. Expected keys include:
            - 'q' (list): The search query string (mandatory).

    Returns:
        dict: A dictionary containing the following keys:
            - "data": A list of matching artworks (if found).
            - "status": HTTP status code (200 for success, 404 for errors).

    Example: >>> await search_artworks({"q": ["monet"]})
        {"data": [...], "status": 200}

    Logs:
        Logs the search query and any exceptions encountered.

    Errors:
        - Returns an error message with status 404 if the search query is missing or no results are found.
    """
    try:
        search_query = params['q'][0]
    except IndexError:
        return {"error": "Artwork not found", 'status':404}
    except KeyError:
        return {"error": "Artwork not found", 'status': 404}

    query_params = {
        "q": search_query,
    }

    response = await handle_get_request(get_app_instance().config.ARTWORKS_SEARCH_API, query_params)

    try:
        return {"data": response['data']['data'], "status": 200}
    except Exception as exception:
        logger.error("search_artworks exception: %s", exception)
        return {"error": "Artwork not found", 'status': 404}

async def get_artworks_recommendations():
    """
    Generate artwork recommendations based on user preferences.

    The function retrieves all artworks from the database and filters them based on the user's preferences.
    It also computes diversity by considering the temporal proximity of artworks.

    User preferences include:
        - `style_title`: The artistic style of the artwork (e.g., "Post-Impressionism").
        - `medium_display`: The medium used in the artwork (e.g., "Oil on canvas").
        - `category_titles`: Categories associated with the artwork (e.g., "Painting and Sculpture of Europe").

    Recommendations are returned as a list of artworks sorted by temporal proximity to the user's average preferred time period.

    Returns:
        dict: A dictionary containing either:
              - "recommendations" (list): A list of recommended artworks with details.
              - "status" (int): HTTP status code.
              - OR "error" (str): An error message in case of failure.
    """
    try:
        # Fetch all artworks from the database
        async with in_transaction() as conn:
            artworks = await Artwork.all().values()

        # Convert database records to a Pandas DataFrame
        artworks_df = pandas.DataFrame(artworks)

        # Handle edge case if no artworks exist
        if artworks_df.empty:
            return {"recommendations": [], 'status': 200}

        # Filter artworks based on user preferences
        filtered_artworks = artworks_df[
            (artworks_df["style_title"] == user_preferences["style_title"]) |
            (artworks_df["medium_display"] == user_preferences["medium_display"]) |
            (artworks_df["category_titles"].apply(lambda x: any(cat in x for cat in user_preferences["category_titles"])))
        ]

        # Compute diversity by time period
        if "date_start" in artworks_df.columns and "date_end" in artworks_df.columns:
            # Calculate avg_date for the entire DataFrame
            artworks_df["avg_date"] = artworks_df[["date_start", "date_end"]].mean(axis=1, skipna=True)

            # Add avg_date to the filtered DataFrame
            filtered_artworks = filtered_artworks.copy()
            filtered_artworks["avg_date"] = filtered_artworks[["date_start", "date_end"]].mean(axis=1, skipna=True)

            # Calculate user_date_preference based on filtered artworks
            user_date_preference = filtered_artworks["avg_date"].mean()

            # Compute date_similarity for filtered artworks
            filtered_artworks["date_similarity"] = numpy.abs(filtered_artworks["avg_date"] - user_date_preference)

            # Add a scoring system to prioritize matches
            filtered_artworks["score"] = (
                    (filtered_artworks["style_title"] == user_preferences["style_title"]).astype(
                        int) * 3 +  # High priority
                    (filtered_artworks["medium_display"] == user_preferences["medium_display"]).astype(
                        int) * 2 +  # Medium priority
                    (filtered_artworks["category_titles"].apply(
                        lambda x: any(cat in x for cat in user_preferences["category_titles"]))).astype(int)
            # Low priority
            )

            # Sort first by score, then by temporal similarity
            filtered_artworks = filtered_artworks.sort_values(by=["score", "date_similarity"], ascending=[False, True]).head(5)

        # Format the response
        recommendations = filtered_artworks[
            ["id", "title", "artist_title", "style_title", "medium_display", "thumbnail"]
        ].to_dict(orient="records")

        return {"recommendations": recommendations, 'status': 200}
    except Exception as exception:
        logger.error("get_artworks_recommendations exception: %s", exception)
        return {"error": "Artwork not found", 'status': 404}