from django.shortcuts import render  # ⭐ AJOUTER CET IMPORT
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Utilisateur
from .serializers import UtilisateurSerializer

class UtilisateurViewSet(viewsets.ModelViewSet):
    queryset = Utilisateur.objects.all()
    serializer_class = UtilisateurSerializer

@api_view(['POST'])
def inscription(request):
    username = request.data.get('username')
    password = request.data.get('password')
    email = request.data.get('email')
    role = request.data.get('role', 'fan')
    
    utilisateur = Utilisateur.objects.create_user(
        username=username, 
        email=email, 
        password=password,
        role=role
    )
    
    return Response({"message": f"{role} créé avec succès"}, status=status.HTTP_201_CREATED)

def page_inscription(request):
    return render(request, 'utilisateur/inscription.html')