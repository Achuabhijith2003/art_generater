from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Now environment variables can be accessed via os.environ
GEMINI_API = os.getenv("GEMINI_API")

