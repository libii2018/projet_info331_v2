from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'utilisateurs', views.UtilisateurViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('inscription/', views.inscription, name='inscription'),
]