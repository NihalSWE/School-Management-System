# In backend/views.py
from django.http import JsonResponse
from .models import Users as Profile
from .models import Designations
from django.contrib.auth.models import User
from django.db import transaction

# DRF Imports
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

# Serializer Imports
from .serializers import AuthUserSerializer, ProfileSerializer


# --- 2. New Registration View (No Change) ---
class RegisterAPIView(APIView):
    permission_classes = [] 
    @transaction.atomic
    def post(self, request):
        auth_serializer = AuthUserSerializer(data=request.data)
        if not auth_serializer.is_valid():
            return Response(auth_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = auth_serializer.save()
        profile_data = request.data
        profile_data['id'] = user.id
        profile_serializer = ProfileSerializer(data=profile_data)
        if not profile_serializer.is_valid():
            transaction.set_rollback(True)
            return Response(profile_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        profile_serializer.save()
        return Response(
            {"message": "User registered successfully"}, 
            status=status.HTTP_201_CREATED
        )

# --- 3. ViewSet for 'auth.User' (No Change) ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AuthUserSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- 4. ViewSet for 'backend.Users' (No Change) ---
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

