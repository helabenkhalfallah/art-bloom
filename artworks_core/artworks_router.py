from sanic import Blueprint, json

from .artworks_data_reader import get_artworks_by_params, get_artwork_by_id, search_artworks, get_artworks_recommendations

# Create a Blueprint for the routes
artworks_router = Blueprint("artworks_router")

@artworks_router.get("/")
async def handle_fallback(request):
    """
    The fallback endpoint when trying to access a non-existent path.

    Args:
        request (sanic.Request): The HTTP request object.

    Returns:
        sanic.response: JSON response indicating that the path does not exist.
    """
    return json({"message": "This path does not exist."}, status=404)

@artworks_router.get("/artworks")
async def get_artworks(request):
    """
    Handles requests to /artworks and returns artwork data based on query parameters.

    Args:
        request (sanic.Request): The HTTP request object containing query parameters.

    Returns:
        sanic.response: JSON response with artwork data or an error message.
    """
    result = await get_artworks_by_params(request.args)
    return json(result)

@artworks_router.get("/artworks/<artwork_id>")
async def get_artwork_by_id_route(request, artwork_id):
    """
    Handles requests to /artworks/<artwork_id> and returns a single artwork's data.

    Args:
        request (sanic.Request): The HTTP request object.
        artwork_id (str): The ID of the artwork to retrieve.

    Returns:
        sanic.response: JSON response with the artwork data or an error message.
    """
    result = await get_artwork_by_id(artwork_id)
    if result:
        return json(result)
    return json({"error": "Artwork not found"}, status=404)

@artworks_router.get("/artworks/search")
async def search_artworks_route(request):
    """
    Handles requests to /artworks/search and returns artwork data based on search criteria.

    Args:
        request (sanic.Request): The HTTP request object containing search parameters.

    Returns:
        sanic.response: JSON response with matching artwork data or an error message.
    """
    result = await search_artworks(request.args)
    return json(result)

@artworks_router.get("/artworks/recommendations")
async def get_artworks_recommendations_route(request):
    """
    Generate artwork recommendations based on user preferences.

    Args:
        request (sanic.Request): The HTTP request object.

    Returns:
        sanic.response: JSON response with recommended artworks.
    """
    result = await get_artworks_recommendations()
    return json(result)