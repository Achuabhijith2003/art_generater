from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now environment variables can be accessed via os.environ
GEMINI_API = os.getenv("GEMINI_API")
CLOUDINARY_CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
CLOUDINARY_API_KEY = os.getenv("CLOUDINARY_API_KEY")
CLOUDINARY_API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

