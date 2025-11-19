from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Oeuvre, Musique, ArtVisuel, Categorie
from .serializers import (
    OeuvreFeedSerializer, 
    MusiqueCreateSerializer, 
    ArtVisuelCreateSerializer,
    CategorieSerializer
)

class OeuvreViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Vue en lecture seule pour le fil d'actualité général (Mixte).
    Fonctionnalité : Recherche et Filtres.
    """
    queryset = Oeuvre.objects.all().order_by('-date_creation')
    serializer_class = OeuvreFeedSerializer
    permission_classes = [permissions.AllowAny]
    
    # Fonctionnalités de recherche
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['categories__slug', 'artiste__username'] # Filtre exact (?categories__slug=makossa)
    search_fields = ['titre', 'description', 'artiste__username'] # Barre de recherche

class MusiqueViewSet(viewsets.ModelViewSet):
    """Vue pour gérer (CRUD) les musiques spécifiquement"""
    queryset = Musique.objects.all()
    serializer_class = MusiqueCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Fonctionnalité : Assigner automatiquement l'artiste connecté
        serializer.save(artiste=self.request.user)

class ArtVisuelViewSet(viewsets.ModelViewSet):
    """Vue pour gérer (CRUD) les arts visuels"""
    queryset = ArtVisuel.objects.all()
    serializer_class = ArtVisuelCreateSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(artiste=self.request.user)