from tortoise import Tortoise

from artworks_settings import get_tortoise_config
from .app_logger import logger

async def init_database():
    """
    Initializes the database connection and generates schemas.

    This function performs the following steps:
        1. Initializes the Tortoise ORM using the configuration provided
           by `get_tortoise_config`.
        2. Generates database schemas based on the defined Tortoise models.
        3. Logs the success or failure of the initialization process.

    Raises:
        Exception: If an error occurs during database initialization, it is logged
                   and then re-raised.

    Example Usage:
        ```
        import asyncio
        from your_module import init_database

        asyncio.run(init_database())
        ```

    Returns:
        None
    """
    try:
        # Initialize the Tortoise ORM with the provided configuration
        await Tortoise.init(config=get_tortoise_config())

        # Generate database schemas
        await Tortoise.generate_schemas()

        # Log success message
        logger.info("Database connected successfully!")
    except Exception as error:
        # Log any errors that occur during initialization
        logger.error("Error during database initialization: %s", error)

        # Raise the error for the caller to handle
        raise
