from rest_framework import serializers
from .models import Categorie, Oeuvre, Musique, ArtVisuel
from comptes.serializers import ArtisteSerializer # Assurez-vous que cela existe

class CategorieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categorie
        fields = ['id', 'nom', 'slug']

# --- SERIALIZERS SPÉCIFIQUES (Pour créer/modifier) ---

class MusiqueCreateSerializer(serializers.ModelSerializer):
    """Utilisé quand un artiste upload une musique"""
    class Meta:
        model = Musique
        fields = '__all__' # Inclut titre, fichier_audio, duree_secondes, etc.
        read_only_fields = ['artiste', 'date_creation'] # L'artiste est auto-assigné par la vue

class ArtVisuelCreateSerializer(serializers.ModelSerializer):
    """Utilisé quand un artiste upload une peinture"""
    class Meta:
        model = ArtVisuel
        fields = '__all__'
        read_only_fields = ['artiste', 'date_creation']

# --- SERIALIZER POLYMORPHE (Pour la lecture/Le fil d'actu) ---

class OeuvreFeedSerializer(serializers.ModelSerializer):
    """
    Ce serializer est magique : il adapte la réponse selon le type d'oeuvre.
    """
    artiste = ArtisteSerializer(read_only=True)
    categories = CategorieSerializer(many=True, read_only=True)
    # Champs spécifiques calculés
    details_specifiques = serializers.SerializerMethodField()

    class Meta:
        model = Oeuvre
        fields = ['id', 'type', 'titre', 'image_couverture', 'artiste', 'categories', 'date_creation', 'details_specifiques']

    def get_details_specifiques(self, obj):
        # Utilise votre méthode get_type() définie dans le modèle
        type_oeuvre = obj.get_type()
        
        if type_oeuvre == 'MUSIQUE':
            musique = obj.musique
            return {
                'url_audio': musique.fichier_audio.url if musique.fichier_audio else None,
                'duree': musique.get_duree_formattee(),
                'producteur': musique.producteur
            }
        elif type_oeuvre == 'VISUEL':
            visuel = obj.artvisuel
            return {
                'prix': visuel.get_prix_display(),
                'dimensions': visuel.dimensions,
                'est_a_vendre': visuel.est_a_vendre
            }
        return None