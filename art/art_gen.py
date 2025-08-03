import os
import io
import google.generativeai as genai
from google.genai import types
import cloudinary
import cloudinary.uploader
from .util.config import GEMINI_API, CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET

# ==============================================================================
#  1. CONFIGURE EXTERNAL LIBRARIES
# ==============================================================================
# This section securely configures the API clients using environment variables.
# This is the standard and secure method for handling secret keys.

# --- Configure Google Generative AI ---
try:
    # The API key is loaded from environment variables for security.
    api_key = GEMINI_API
    if not api_key:
        raise ValueError("GOOGLE_API_KEY environment variable not set.")
    genai.configure(api_key=api_key)
    print("Successfully configured Google Generative AI.")
except Exception as e:
    print(f"CRITICAL ERROR: Failed to configure Google API. Details: {e}")

# --- Configure Cloudinary for Image Hosting ---
try:
    cloudinary.config(
      cloud_name=CLOUDINARY_CLOUD_NAME,
      api_key=CLOUDINARY_API_KEY,
      api_secret=CLOUDINARY_API_SECRET,
      secure=True
    )
    print("Successfully configured Cloudinary.")
except Exception as e:
    print(f"CRITICAL ERROR: Failed to configure Cloudinary. Details: {e}")


# ==============================================================================
#  2. DEFINE THE CORE GENERATION FUNCTION (STREAMING)
# ==============================================================================


# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import mimetypes
import os
from google import genai
from google.genai import types


def save_binary_file(file_name, data):
    f = open(file_name, "wb")
    f.write(data)
    f.close()
    print(f"File saved to to: {file_name}")


def generate(prompt: str):
    client = genai.Client(
        api_key=GEMINI_API,
    )

    model = "gemini-2.0-flash-preview-image-generation"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=prompt),
            ],
        ),
    ]
    generate_content_config = types.GenerateContentConfig(
        response_modalities=[
            "IMAGE",
            "TEXT",
        ],
    )

    file_index = 0
    for chunk in client.models.generate_content_stream(
        model=model,
        contents=contents,
        config=generate_content_config,
    ):
        if (
            chunk.candidates is None
            or chunk.candidates[0].content is None
            or chunk.candidates[0].content.parts is None):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"ENTER_FILE_NAME_{file_index}"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            print(f"Received image data with MIME type: {inline_data.mime_type}")
            # save_binary_file(f"{file_name}{file_extension}", data_buffer)
            print("Uploading image to Cloudinary...")
            upload_result = cloudinary.uploader.upload(data_buffer)
        
            image_url = upload_result.get('secure_url')
            if not image_url:
                raise ValueError("Cloudinary upload did not return a secure_url.")
            
            print(f"Image upload successful. URL: {image_url}")

        # --- Step 4: Return the final results ---
            return image_url
        else:
            print(chunk.text)



# def generate(prompt: str):
#     """
#     Generates text and an image from a prompt using a streaming call,
#     and uploads the resulting image to Cloudinary.

#     Args:
#         prompt: The user-submitted text prompt.

#     Returns:
#         A tuple containing (image_url, generated_text).
#         Returns (None, "Error message...") on failure.
#     """
#     print(f"Starting streaming generation for prompt: '{prompt}'")

#     try:
#         # --- Step 1: Set up the model and generation request ---
#         model = genai.GenerativeModel("gemini-2.0-flash-preview-image-generation")
        
#         contents = [
#             types.Content(
#                 role="user",
#                 parts=[genai.Part.from_text(text=prompt)],
#             ),
#         ]
        
#         generation_config = types.GenerateContentConfig(
#             response_modalities=["IMAGE", "TEXT"],
#         )

#         # --- Step 2: Process the streaming response ---
#         print("Sending request to Google AI model and processing stream...")
#         response_stream = model.generate_content(
#             contents=contents,
#             generation_config=generation_config,
#             stream=True
#         )

#         generated_text = ""
#         image_bytes = None

#         # Iterate through the chunks of data as they arrive
#         for chunk in response_stream:
#             if chunk.text:
#                 generated_text += chunk.text
            
#             # Check for image data in the chunk's parts
#             if chunk.candidates and chunk.candidates[0].content and chunk.candidates[0].content.parts:
#                 for part in chunk.candidates[0].content.parts:
#                     if part.inline_data and part.inline_data.data:
#                         image_bytes = part.inline_data.data
#                         print("Image data received in stream.")
        
#         if not generated_text or not image_bytes:
#             raise ValueError("AI stream did not yield both text and image data.")
        
#         print("Successfully processed stream and extracted text and image data.")

#         # --- Step 3: Upload the final image bytes to Cloudinary ---
#         print("Uploading image to Cloudinary...")
#         upload_result = cloudinary.uploader.upload(image_bytes)
        
#         image_url = upload_result.get('secure_url')
#         if not image_url:
#             raise ValueError("Cloudinary upload did not return a secure_url.")
            
#         print(f"Image upload successful. URL: {image_url}")

#         # --- Step 4: Return the final results ---
#         return image_url, generated_text

#     except Exception as e:
#         # Catch any error during the process and return a user-friendly message.
#         error_message = f"An error occurred in the generation process: {e}"
#         print(error_message)
#         return None, error_message
