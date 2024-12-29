import asyncio
import platform
import signal

from tortoise.exceptions import DBConnectionError

from artworks_settings import initialize_app_env
from artworks_core import  artworks_router
from artworks_utils import logger, init_database

# Initialize and retrieve the Sanic app instance
app = initialize_app_env()

# Register the router
app.blueprint(artworks_router)

async def init_app_task():
    """
    Asynchronous initialization for the app, such as database setup.

    Performs:
        - Database connection initialization.
        - Schema generation (if required).

    Logs:
        - Success or failure of the initialization process.
    """
    try:
        logger.info("Initializing ArtBloom %s", "🚀")
        await init_database()
        logger.info("Database initialized!")
    except DBConnectionError as db_error:
        logger.error("Database connection error during initialization: %s", db_error)
    except Exception as error:
        logger.error("Unexpected error during initialization: %s", error)
        raise  # Re-raise unexpected exceptions for further handling

async def update_data_task():
    """
    Periodically updates the artworks database.

    Performs:
        - Fetches the latest artwork data from the external API.
        - Updates the local database with new or modified records.

    Logs:
        - Success or failure of the update process.
    """
    try:
        logger.info("Starting update_data...")
        # Uncomment the following line to enable periodic updates:
        # await update_artworks()
        logger.info("Finished update_data!")
    except asyncio.TimeoutError as timeout_error:
        logger.error("Timeout occurred during update_data: %s", timeout_error)
    except Exception as error:
        logger.error("Unexpected error during update_data: %s", error)
        raise  # Re-raise unexpected exceptions for further handling

async def run_server_task():
    """
    Run the Sanic app using the asynchronous API.

    Performs:
        - Starts the Sanic server asynchronously.
        - Handles server shutdown gracefully when cancelled.

    Logs:
        - Server startup and shutdown details.

    Raises:
        asyncio.CancelledError: If the task is cancelled during runtime.
    """
    server = await app.create_server(
        host=app.config.HOST,
        port=app.config.PORT,
        debug=app.config.DEBUG,
        return_asyncio_server=True,
    )
    try:
        logger.info("Starting Sanic server...")
        await server.startup()  # Explicitly start the server
        logger.info("Sanic server started.")
        await server.serve_forever()  # Start serving requests
    except asyncio.CancelledError:
        logger.info("Server task cancelled. Shutting down...")
        server.close()  # Stop accepting new connections
        await server.wait_closed()  # Wait for all connections to close
        logger.info("Sanic server shutdown complete.")
        raise

async def main():
    """
    Main entry point for running the application.

    Performs:
        - Initializes the application (e.g., database setup).
        - Starts the Sanic server and the periodic update task.
        - Waits for shutdown signals and cancels all tasks gracefully.

    Logs:
        - Startup and shutdown events.
        - Task cancellations and exceptions.

    Handles:
        - Unix signal handlers (SIGINT, SIGTERM) for graceful shutdown.
        - KeyboardInterrupt for manual shutdown.
    """
    tasks = []
    stop_event = asyncio.Event()

    def shutdown_signal_handler():
        """
        Handles shutdown signals (e.g., SIGINT, SIGTERM) and sets the stop event.
        """
        logger.info("Shutdown signal received.")
        stop_event.set()

    try:
        # Add signal handlers on Unix-based systems
        if platform.system() != "Windows":
            for sig in (signal.SIGINT, signal.SIGTERM):
                asyncio.get_event_loop().add_signal_handler(sig, shutdown_signal_handler)

        # Initialize application (e.g., database, tasks)
        await init_app_task()

        # Schedule server task
        server_task = asyncio.create_task(run_server_task())
        tasks.append(server_task)

        # Schedule update task
        update_task = asyncio.create_task(update_data_task())
        tasks.append(update_task)

        # Wait for shutdown signal or KeyboardInterrupt
        try:
            await stop_event.wait()
        except KeyboardInterrupt:
            logger.info("Keyboard interrupt received. Shutting down...")
            stop_event.set()
    except asyncio.CancelledError:
        logger.info("Cancelling all tasks...")
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)
        logger.info("Shutdown complete.")

if __name__ == "__main__":
    # Entry point for starting the ArtBloom server.
    logger.info("Starting ArtBloom server %s", "🚀🎉")
    asyncio.run(main())
