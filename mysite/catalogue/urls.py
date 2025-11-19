# backend/urls.py ou catalogue/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from catalogue.views import OeuvreViewSet, MusiqueViewSet, ArtVisuelViewSet

router = DefaultRouter()
router.register(r'feed', OeuvreViewSet, basename='feed') # http://.../api/feed/
router.register(r'musiques', MusiqueViewSet)             # http://.../api/musiques/
router.register(r'arts-visuels', ArtVisuelViewSet)       # http://.../api/arts-visuels/

urlpatterns = [
    path('api/', include(router.urls)),
]