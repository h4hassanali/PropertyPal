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
    path('aboutus',aboutus,name='aboutus'),
    path('advanced_search',advanced_search,name='advanced_search'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
