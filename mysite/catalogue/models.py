from django.db import models
from django.conf import settings # Pour lier à l'utilisateur

class Categorie(models.Model):
    nom = models.CharField(max_length=50) # Ex: Makossa, Afropop, Art Abstrait
    slug = models.SlugField(unique=True)

class Oeuvre(models.Model):
    """
    Table parent : contient les infos communes à TOUS les arts.
    """
    artiste = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='oeuvres')
    titre = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    image_couverture = models.ImageField(upload_to='covers/') # Pochette album ou photo de la peinture
    date_creation = models.DateTimeField(auto_now_add=True)
    categories = models.ManyToManyField(Categorie)

    # Cette astuce permet de savoir quel type d'enfant c'est
    def get_type(self):
        if hasattr(self, 'musique'):
            return 'MUSIQUE'
        elif hasattr(self, 'artvisuel'):
            return 'VISUEL'
        return 'GENERIQUE'

    def __str__(self):
        return self.titre

class Musique(Oeuvre):
    """
    Table enfant : Spécifique aux fichiers audio
    """
    fichier_audio = models.FileField(upload_to='musique/')
    duree_secondes = models.IntegerField()
    producteur = models.CharField(max_length=100, blank=True)
    # Hérite automatiquement de titre, artiste, image_couverture...

    def get_duree_formattee(self):
        """Convertit 230 secondes en '03:50'"""
        minutes = self.duree_secondes // 60
        secondes = self.duree_secondes % 60
        return f"{minutes:02d}:{secondes:02d}"

class ArtVisuel(Oeuvre):
    """
    Table enfant : Spécifique Peinture, Photo, Sculpture
    """
    image_hd = models.ImageField(upload_to='art_visuel_hd/') # L'oeuvre elle-même
    dimensions = models.CharField(max_length=50) # Ex: 120x80cm
    est_a_vendre = models.BooleanField(default=False)
    prix_fcfa = models.DecimalField(max_digits=10, decimal_places=0, null=True, blank=True)

    def get_prix_display(self):
        """Affiche '50 000 FCFA' ou 'Gratuit'"""
        if self.est_a_vendre and self.prix_fcfa:
            # Format avec séparateur de milliers
            return f"{self.prix_fcfa:,} FCFA".replace(',', ' ')
        return "Non à vendre"