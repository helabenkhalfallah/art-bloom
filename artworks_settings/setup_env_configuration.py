"""
This module contains configuration setup for the ArtBloom application.

This module manages the configuration for the ArtBloom application by loading environment
variables and applying them to the Sanic app's configuration.

It utilizes `dotenv` to load environment variables from a `.env` file, ensuring that the
application's artworks_settings are dynamic and configurable without hardcoding sensitive data
like secrets or database URLs.

Functions:
    - update_configuration(app): Updates the Sanic app's configuration with environment variables.

Environment Variables:
    - APP_NAME: The name of the application (default: "DefaultAppName").
    - DEBUG: Enables or disables debug mode (default: "False").
    - DATABASE_URL: The database connection string.
    - SECRET_KEY: The secret key for securing the application.
    - APP_PORT: The port number on which the app runs (default: 8000).
    - APP_HOST: The host interface for the app (default: "0.0.0.0").
"""
import os
from sanic import Sanic
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Global application instance
current_app = None

def initialize_app_env():
    """
    Initializes the global Sanic application instance.

    Returns:
        Sanic: The globally initialized Sanic app instance.
    """
    global current_app
    if current_app is None:
        current_app = Sanic("ArtBloom")
        set_env_configuration(current_app)
    return current_app

def set_env_configuration(app):
    """
    Updates the configuration of the given Sanic application using environment variables.

    Parameters:
        app (Sanic): The Sanic application instance to configure.

    Notes:
    - Ensure that a `.env` file exists in the project root with the necessary environment variables.
    - Missing variables will fall back to their default values if provided.
    """
    app.config.APP_NAME = os.getenv("APP_NAME", "DefaultAppName")
    app.config.DEBUG = os.getenv("DEBUG", "False").lower() in ("true", "1")
    app.config.DATABASE_URL = os.getenv("DATABASE_URL")
    app.config.SECRET_KEY = os.getenv("SECRET_KEY")
    app.config.PORT = int(os.getenv("APP_PORT", "8000"))  # Default to port 8000
    app.config.HOST = os.getenv("APP_HOST", "0.0.0.0")  # Default to all interfaces
    app.config.ARTWORKS_API = os.getenv("ARTWORKS_API", "")  # Default to an empty string
    app.config.ARTWORKS_SEARCH_API = os.getenv("ARTWORKS_SEARCH_API", "")  # Default to an empty string

def get_app_instance():
    """
    Returns the globally initialized Sanic app instance.

    Raises:
        RuntimeError: If the application instance is not yet initialized.
    """
    if current_app is None:
        raise RuntimeError("Application configuration has not been initialized.")
    return current_app