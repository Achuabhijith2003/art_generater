# art/views.py

from django.shortcuts import render
from .art_gen import generate
import os

def art_generator_view(request):
    art_filename = None
    prompt = request.GET.get('prompt', None)

    if prompt:
        print(f"Received prompt: {prompt}")
        # The generate() function returns the full path
        full_path = generate(prompt)
        print(f"Generated art saved at: {full_path}")

        # We only need the filename for the template
        if full_path:
            # Use os.path.basename for a reliable way to get the filename
            art_filename = os.path.basename(full_path)

    # The view will now render the page on both initial load and after a GET request
    return render(request, 'index.html', {'art': art_filename})