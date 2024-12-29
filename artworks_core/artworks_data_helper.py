async def format_artworks_by_params(data, params):
    """
    Formats and sorts a list of artworks based on query parameters.

    Args:
        data (list): List of artwork dictionaries to be formatted.
        params (dict): Query parameters containing sorting preferences.

    Returns:
        list: A sorted list of artworks based on the specified sort type, or the original list if no valid sort type is provided.
    """
    if not data:
        return []

    # Extract sorting type from query parameters
    try:
        sort_type = params['sort'][0]
    except KeyError:
        sort_type = None

    # Define sorting rules
    sorting_rules = {
        "date_asc": lambda x: x.get("date_start", 0),
        "date_desc": lambda x: x.get("date_start", 0),
        "title_asc": lambda x: x.get("title", "").lower(),
        "title_desc": lambda x: x.get("title", "").lower(),
        "artist_title_asc": lambda x: x.get("artist_title", "").lower(),
        "artist_title_desc": lambda x: x.get("artist_title", "").lower(),
        "artist_display_asc": lambda x: x.get("artist_display", "").lower(),
        "artist_display_desc": lambda x: x.get("artist_display", "").lower(),
    }

    # Apply sorting if valid sort_type is provided
    if sort_type in sorting_rules:
        reverse = "desc" in sort_type  # Check if descending order is required
        return sorted(data, key=sorting_rules[sort_type], reverse=reverse)

    # Return original data if no valid sort_type
    return data
