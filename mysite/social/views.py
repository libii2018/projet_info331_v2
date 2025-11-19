from rest_framework import viewsets, permissions, status, views
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Commentaire, Soutien
from .serializers import CommentaireSerializer
from catalogue.models import Oeuvre

class CommentaireViewSet(viewsets.ModelViewSet):
    """
    Gère le CRUD des commentaires.
    """
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        # Associe automatiquement le commentaire à l'utilisateur connecté
        serializer.save(auteur=self.request.user)

    def get_queryset(self):
        # Optionnel : Permet de filtrer les commentaires par oeuvre (?oeuvre_id=12)
        queryset = super().get_queryset()
        oeuvre_id = self.request.query_params.get('oeuvre_id')
        if oeuvre_id:
            queryset = queryset.filter(oeuvre_id=oeuvre_id)
        return queryset

class ToggleSoutienView(views.APIView):
    """
    Vue spéciale pour le bouton 'Like'.
    Fonctionne comme un interrupteur (Toggle).
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, oeuvre_id):
        oeuvre = get_object_or_404(Oeuvre, pk=oeuvre_id)
        user = request.user

        # On cherche si le like existe déjà
        soutien_existant = Soutien.objects.filter(fan=user, oeuvre=oeuvre).first()

        if soutien_existant:
            # Si oui, on le supprime (Unlike)
            soutien_existant.delete()
            return Response(
                {"message": "Soutien retiré", "a_like": False, "nouveau_total": oeuvre.soutiens.count()},
                status=status.HTTP_200_OK
            )
        else:
            # Si non, on le crée (Like)
            Soutien.objects.create(fan=user, oeuvre=oeuvre)
            return Response(
                {"message": "Soutien ajouté", "a_like": True, "nouveau_total": oeuvre.soutiens.count()},
                status=status.HTTP_201_CREATED
            )