from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .art_gen import generate  # Assuming this is the function to generate art

# Create your views here.

# user_chat=['hi', 'hello', 'how are you?']
# art_chat=['hlo', 'hlo', ' are you?']
# user_chat=[]
# art_chat=[]

# for i in range(len(user_chat)):
#     print(f"User: {user_chat[i]}")
#     print(f"Art: {art_chat[i]}")

class ArtView:
    def get( request):
        if request.method == 'GET':
            # Handle GET request logic here
            prompt=request.GET.get('prompt')
            if prompt:
                print(f"Received prompt: {prompt}")
                full_path=generate(prompt)  # Call the generate function with the prompt
                # full_path='generated\generated_image_0.png'
                print(f"Generated art saved at: {full_path}")
        return render(request, 'index.html', {'art': full_path})
    def index(request):
        # Handle POST request logic here
        return render(request, 'index.html', {})

