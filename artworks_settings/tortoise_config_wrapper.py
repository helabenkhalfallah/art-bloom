
from dotenv import load_dotenv

from artworks_settings import get_tortoise_config

# Load environment variables
load_dotenv()

# Evaluate the dynamic Tortoise configuration and expose it as a dictionary
TORTOISE_ORM = get_tortoise_config()