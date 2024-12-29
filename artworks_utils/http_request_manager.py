import asyncio
import httpx

from .app_logger import logger

async def handle_get_request(api_url, params):
    """
    Handles an HTTP GET request to the specified API URL with query parameters.

    This function performs the following steps:
        1. Sends an asynchronous HTTP GET request using `httpx.AsyncClient`.
        2. Handles various exceptions, including timeout, HTTP errors, and generic errors.
        3. Logs errors for debugging purposes and provides a structured JSON response.

    Args:
        api_url (str): The target API endpoint URL.
        params (dict): Query parameters to include in the GET request.

    Returns:
        dict: A dictionary containing:
            - "data" (dict): The response payload or an error message.
            - "status" (int): The HTTP status code of the response.

    Raises:
        asyncio.CancelledError: Propagates cancellation for proper task handling.

    Example Usage:
        ```
        response = await handle_get_request(
            "https://api.example.com/resource",
            {"param1": "value1", "param2": "value2"}
        )
        if response["status"] == 200:
            print("Success:", response["data"])
        else:
            print("Error:", response["data"]["error"])
        ```

    Exception Handling:
        - **TimeoutException**: Occurs if the request exceeds the timeout limit.
        - **RequestError**: Handles connection-related errors.
        - **HTTPStatusError**: Handles unexpected HTTP status codes.
        - **Generic Exception**: Handles all other unexpected errors.

    Notes:
        - The function uses a 60-second timeout for the HTTP GET request.
        - It propagates `asyncio.CancelledError` to ensure proper coroutine cancellation.

    """
    try:
        # Perform an asynchronous GET request with a 60-second timeout
        async with httpx.AsyncClient() as client:
            response = await client.get(api_url, params=params, timeout=60)
            response.raise_for_status()  # Raise an exception for HTTP errors
            return {"data": response.json(), "status": 200}

    except asyncio.CancelledError:
        # Propagate task cancellation for proper handling
        raise

    except httpx.TimeoutException as exception:
        # Handle request timeout
        logger.error("TimeoutException during handle_get_request: %s", exception)
        return {
            "data": {"error": "The request timed out while accessing the list of Artworks"},
            "status": 504,
        }

    except httpx.RequestError as exception:
        # Handle request-related errors (e.g., connection issues)
        logger.error("RequestError during handle_get_request: %s", exception)
        return {
            "data": {"error": "A request error occurred while accessing the list of Artworks"},
            "status": 500,
        }

    except httpx.HTTPStatusError as exception:
        # Handle HTTP status errors
        logger.error("HTTPStatusError during handle_get_request: %s", exception)
        return {
            "data": {"error": "An HTTP error occurred while accessing the list of Artworks"},
            "status": exception.response.status_code,
        }

    except Exception as exception:
        # Handle any other unexpected exceptions
        logger.error("Exception during handle_get_request: %s", exception)
        return {
            "data": {"error": "An unknown error occurred"},
            "status": 500,
        }
