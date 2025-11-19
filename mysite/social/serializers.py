from rest_framework import serializers
from .models import Commentaire, Soutien
from catalogue.models import Oeuvre

class CommentaireSerializer(serializers.ModelSerializer):
    # On veut le nom de l'auteur, pas juste son ID 1, 2 ou 3
    auteur_nom = serializers.ReadOnlyField(source='auteur.username')
    
    class Meta:
        model = Commentaire
        fields = ['id', 'oeuvre', 'auteur_nom', 'texte', 'date']
        read_only_fields = ['date', 'auteur_nom']

class SoutienSerializer(serializers.ModelSerializer):
    class Meta:
        model = Soutien
        fields = '__all__'