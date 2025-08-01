# To run this code you need to install the following dependencies:
# pip install google-genai

import base64
import mimetypes
import os
from google import genai
from google.genai import types
from .util.config import GEMINI_API
import random


def save_binary_file(file_name, data):
    full_path = os.path.join('generated', file_name)
    try:
        # Open the file in write-binary mode ("wb").
        with open(full_path, "wb") as f:
            f.write(data)
        print(f"File successfully saved to: {full_path}")
        return full_path
    except IOError as e:
        print(f"Error saving file: {e}")
    # f = open(file_name, "wb",)
    # f.write(data)
    print(f"File saved to to: {file_name}")


def generate(promt):
    client = genai.Client(
        api_key=GEMINI_API,
    )

    model = "gemini-2.0-flash-preview-image-generation"
    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=promt),
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
            or chunk.candidates[0].content.parts is None
        ):
            continue
        if chunk.candidates[0].content.parts[0].inline_data and chunk.candidates[0].content.parts[0].inline_data.data:
            file_name = f"{random.randint(10000, 99999)}_generated_image"
            file_index += 1
            inline_data = chunk.candidates[0].content.parts[0].inline_data
            data_buffer = inline_data.data
            file_extension = mimetypes.guess_extension(inline_data.mime_type)
            full_path=save_binary_file(f"{file_name}{file_extension}", data_buffer)
            return full_path
        else:
            print(chunk.text)

# if __name__ == "__main__":
#     generate()
#     print(GEMINI_API)
