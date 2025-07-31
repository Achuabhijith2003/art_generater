from django.urls import path, include
from art.views import ArtView

urlpatterns = [
    path('', ArtView.index, name='artgenerator'),
    path('asked/', ArtView.get, name='askart'),
]
