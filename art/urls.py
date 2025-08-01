# art/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # This single path will handle both showing the form and displaying the result
    path('', views.art_generator_view, name='art-generator'),
]