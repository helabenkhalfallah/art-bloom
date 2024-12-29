import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_tortoise_config():
    return {
        "connections": {
            "default": os.getenv("DATABASE_URL"),
        },
        "apps": {
            "models": {
                "models": ["artworks_core.models", "aerich.models"],  # Update with your models
                "default_connection": "default",
            },
        },
    }
