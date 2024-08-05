from django.urls import path, include
from .views import *
from django.conf.urls.static import static
from django.conf import settings

# urls.py
urlpatterns = [
    path('index', index, name='index'),
    path('search', search, name='search'),
    path('autocomplete/', autocomplete, name='autocomplete'),
    path('accessories/', list_accessories, name='list_accessories'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
