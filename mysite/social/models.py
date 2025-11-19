from django.db import models
from django.conf import settings
from catalogue.models import Oeuvre

class Commentaire(models.Model):
    auteur = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oeuvre = models.ForeignKey(Oeuvre, on_delete=models.CASCADE, related_name='commentaires')
    texte = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

class Soutien(models.Model):
    """Pour gérer les likes ou les favoris"""
    fan = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    oeuvre = models.ForeignKey(Oeuvre, on_delete=models.CASCADE, related_name='soutiens')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('fan', 'oeuvre') # Un fan ne peut like qu'une fois