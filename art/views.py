from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .art_gen import generate  # Assuming this is the function to generate art

# Create your views here.

# user_chat=['hi', 'hello', 'how are you?']
# art_chat=['hlo', 'hlo', ' are you?']
user_chat=[]
art_chat=[]

for i in range(len(user_chat)):
    print(f"User: {user_chat[i]}")
    print(f"Art: {art_chat[i]}")

class ArtView:
    def get( request):
        if request.method == 'GET':
            # Handle GET request logic here
            user_chat=[]
            art_chat=[]
            prompt=request.GET.get('prompt')
            if prompt:
                print(f"Received prompt: {prompt}")
                user_chat.append(prompt)
                art_chat.append('Response to: ' + prompt)  # Simulated response
                full_path=generate(prompt)  # Call the generate function with the prompt
                print(f"Generated art saved at: {full_path}")
                art_chat[-1] = full_path
            print(f"User chat: {user_chat} and Art chat: {art_chat}")

            chat_pairs = list(zip(user_chat, art_chat))

        return render(request, 'index.html', {'chat_pairs': chat_pairs})
    def index(request):
        # Handle POST request logic here
        chat_pairs = list(zip(user_chat, art_chat))
        return render(request, 'index.html', {'chat_pairs': chat_pairs})

