# art/urls.py
from django.urls import path
from art.views import ArtView

urlpatterns = [
    # This will now correspond to the URL /art/
    path('', ArtView.index, name='home'),
    path('get/', ArtView.get, name='askart'),
]