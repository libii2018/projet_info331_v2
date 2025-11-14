from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    ROLE_CHOICES = [
        ('fan', 'Fan'),
        ('artiste', 'Artiste'),
        ('admin', 'Administrateur'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='fan')
    telephone = models.CharField(max_length=20, blank=True)
    bio = models.TextField(max_length=500, blank=True)
    date_naissance = models.DateField(null=True, blank=True)
    photo_profil = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"