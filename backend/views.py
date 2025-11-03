# In backend/views.py
from django.http import JsonResponse
from .models import * 
from django.contrib.auth.hashers import check_password

# DRF Imports
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny # <-- We still need this for CustomLoginView

# --- 1. IMPORT OUR TOKEN GENERATOR ---
from .jwt_utils import get_tokens_for_user 

# Serializer Imports
from .serializers import (
    TeacherSerializer, ClassesSerializer, SectionSerializer, 
    SubjectSerializer, StudentSerializer, ParentsSerializer,
    SystemadminSerializer, UserSerializer
)

# --- 2. CUSTOM LOGIN VIEW (This is the only public view) ---
class CustomLoginView(APIView):
    permission_classes = [AllowAny] # This endpoint is public

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = None
        
        # ... (all your "Try" blocks for login are correct, no change) ...
        # Try Teacher table
        try:
            u = Teacher.objects.get(username=username)
            if check_password(password, u.password): user = u
        except Teacher.DoesNotExist: pass

        # Try Student table
        if not user:
            try:
                u = Student.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Student.DoesNotExist: pass

        # Try Parents table
        if not user:
            try:
                u = Parents.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Parents.DoesNotExist: pass
        
        # Try Systemadmin table
        if not user:
            try:
                u = Systemadmin.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Systemadmin.DoesNotExist: pass

        # Try User table (for other staff)
        if not user:
            try:
                u = User.objects.get(username=username)
                if check_password(password, u.password): user = u
            except User.DoesNotExist: pass

        if user:
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)

        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# --- 3. API ViewSets (NOW ALL SECURE) ---
# We REMOVED the CreateUserPermissionMixin.
# All endpoints are now secure by default from settings.py

class TeacherViewSet(viewsets.ModelViewSet):
    queryset = Teacher.objects.all()
    serializer_class = TeacherSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = Student.objects.all()
    serializer_class = StudentSerializer

class ParentsViewSet(viewsets.ModelViewSet):
    queryset = Parents.objects.all()
    serializer_class = ParentsSerializer

class SystemadminViewSet(viewsets.ModelViewSet):
    queryset = Systemadmin.objects.all()
    serializer_class = SystemadminSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ClassesViewSet(viewsets.ModelViewSet):
    queryset = Classes.objects.all()
    serializer_class = ClassesSerializer

class SectionViewSet(viewsets.ModelViewSet):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class SubjectViewSet(viewsets.ModelViewSet):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer