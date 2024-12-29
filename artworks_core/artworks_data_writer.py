import math

from artworks_core.artworks_data_reader import get_total_artworks
from artworks_core.models import Artwork
from artworks_utils import handle_get_request, logger
from artworks_settings import get_app_instance

async def create_if_not_exists(model, **fields):
    """
    Create a record in the database if it does not already exist.

    Args:
        model: The Tortoise model class.
        **fields: The fields to use for existence check and creation.

    Returns:
        Tuple of (instance, created):
            - instance: The retrieved or newly created instance.
            - created: Boolean indicating whether the record was created.
    """
    try:
        # Check for existence
        instance = await model.get_or_none(**fields)
        if instance:
            logger.info("Record with fields %s already exists. Skipping...", fields)
            return instance, False

        # Create the record if it doesn't exist
        instance = await model.create(**fields)
        logger.info("Created new record with fields: %s", fields)
        return instance, True
    except Exception as exception:
        logger.error("Error in create_if_not_exists: %s", exception)
        raise

async def save_artworks_page(data):
    """
    Saves a list of artworks to the database.

    Args:
        data (list): List of artwork dictionaries to be saved.

    Returns:
        list: The input data list for potential further processing.
    """
    logger.info("Saving data: %s artworks", len(data))

    if not data:
        return None

    for item in data:
        artwork_data = {
            "title": item.get("title", "Unknown Title"),
            "artist_title": item.get("artist_title", "Unknown Artist"),
            "place_of_origin": item.get("place_of_origin", "Unknown Origin"),
            "thumbnail": item.get("thumbnail", None),
            "date_start": item.get("date_start", None),
            "date_end": item.get("date_end", None),
            "date_display": item.get("date_display", None),
            "artist_display": item.get("artist_display", None),
            "description": item.get("description", None),
            "short_description": item.get("short_description", None),
            "classification_title": item.get("classification_title", None),
            "style_title": item.get("style_title", None),
            "medium_display": item.get("medium_display", None),
            "material_titles": item.get("material_titles", []),
            "term_titles": item.get("term_titles", []),
            "category_titles": item.get("category_titles", []),
        }

        try:
            artwork, created = await create_if_not_exists(Artwork, **artwork_data)
            if created:
                logger.info("Saved artwork with ID: %s", artwork.id)
            else:
                logger.info("Skipped existing artwork: %s", artwork_data["title"])
        except Exception as exception:
            logger.error("Error saving artwork: %s", exception)

    return data

async def update_artworks():
    """
    Fetches artworks from the Art Institute of Chicago API and saves them to the local database.

    Returns:
        bool: True if the update was successful, False otherwise.
    """
    logger.info("Starting database update")

    page_size = 100
    logger.info("Page size: %s", page_size)

    total_artworks = await get_total_artworks()
    logger.info("Total artworks: %s", total_artworks)

    if total_artworks <= 0:
        logger.warning("No artworks found to update.")
        return False

    total_pages = math.ceil(total_artworks / page_size)  # Ensure correct page calculation
    logger.info("Total pages: %s", total_pages)

    for page in range(1, total_pages + 1):  # Loop through all pages
        logger.info("Processing page: %s", page)

        query_params = {
            "page": page,
            "limit": page_size,
        }

        response = await handle_get_request(get_app_instance().config.ARTWORKS_API, query_params)

        try:
            data = response.get("data", {}).get("data", [])
            await save_artworks_page(data)
        except KeyError as exception:
            logger.error("Data processing error on page %s: %s", page, exception)
            continue
        except Exception as exception:
            logger.error("Unexpected error on page %s: %s", page, exception)
            continue

    logger.info("Database update completed")
    return True
