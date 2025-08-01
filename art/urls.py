from django.urls import path, include
from art.views import ArtView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', ArtView.index, name='artgenerator'),
    path('asked/', ArtView.get, name='askart'),
]

# Only add this during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)