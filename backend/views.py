# In backend/views.py
from django.http import JsonResponse
from .models import * 
from django.contrib.auth.hashers import check_password

# DRF Imports
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

# --- 1. IMPORT ALL PERMISSION CLASSES ---
from .permissions import (
    IsAdminOrReadOnly, IsAdminOrStudentOwner, 
    IsAdminOrTeacherOwner, IsAdminOrParentOwner, IsAdminUser
)
from .jwt_utils import get_tokens_for_user 

# Serializer Imports
from .serializers import (
    TeacherSerializer, ClassesSerializer, SectionSerializer, 
    SubjectSerializer, StudentSerializer, ParentsSerializer,
    SystemadminSerializer, UserSerializer
)

# --- CUSTOM LOGIN VIEW (No Change) ---
class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    # ... (all login code is correct) ...
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({'error': 'Username and password are required'}, status=status.HTTP_400_BAD_REQUEST)
        user = None
        try:
            u = Teacher.objects.get(username=username)
            if check_password(password, u.password): user = u
        except Teacher.DoesNotExist: pass
        if not user:
            try:
                u = Student.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Student.DoesNotExist: pass
        if not user:
            try:
                u = Parents.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Parents.DoesNotExist: pass
        if not user:
            try:
                u = Systemadmin.objects.get(username=username)
                if check_password(password, u.password): user = u
            except Systemadmin.DoesNotExist: pass
        if not user:
            try:
                u = User.objects.get(username=username)
                if check_password(password, u.password): user = u
            except User.DoesNotExist: pass
        if user:
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


# --- API ViewSets ---

class TeacherViewSet(viewsets.ModelViewSet):
    serializer_class = TeacherSerializer
    permission_classes = [IsAdminOrTeacherOwner]
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' or user_type == 'user':
            return Teacher.objects.all()
        if user_type == 'teacher':
            return Teacher.objects.filter(teacherid=user_id) 
        if user_type == 'student' or user_type == 'parent':
            return Teacher.objects.all()
        return Teacher.objects.none() 

class ParentsViewSet(viewsets.ModelViewSet):
    serializer_class = ParentsSerializer
    permission_classes = [IsAdminOrParentOwner]
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']
    
    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' or user_type == 'user':
            return Parents.objects.all()
        if user_type == 'parent':
            return Parents.objects.filter(parentsid=user_id)
        return Parents.objects.none()

# --- 2. APPLY THE FIX HERE ---
class SystemadminViewSet(viewsets.ModelViewSet):
    queryset = Systemadmin.objects.all()
    serializer_class = SystemadminSerializer
    permission_classes = [IsAdminUser] # <-- ADDED
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']

# --- 3. AND APPLY THE FIX HERE ---
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser] # <-- ADDED
    ordering_fields = ['create_date'] 
    ordering = ['-create_date']

class StudentViewSet(viewsets.ModelViewSet):
    serializer_class = StudentSerializer
    permission_classes = [IsAdminOrStudentOwner]
    ordering_fields = ['create_date']
    ordering = ['-create_date']

    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' or user_type == 'user':
            return Student.objects.all()
        if user_type == 'student':
            return Student.objects.filter(studentid=user_id) 
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Student.objects.filter(classesid__in=class_ids)
        return Student.objects.none()


class ClassesViewSet(viewsets.ModelViewSet):
    serializer_class = ClassesSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']

    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' or user_type == 'user':
            return Classes.objects.all()
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Classes.objects.filter(classesid__in=class_ids)
        return Classes.objects.none()


class SectionViewSet(viewsets.ModelViewSet):
    serializer_class = SectionSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']

    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' or user_type == 'user':
            return Section.objects.all()
        if user_type == 'teacher':
            class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
            return Section.objects.filter(classesid__in=class_ids)
        return Section.objects.none()


class SubjectViewSet(viewsets.ModelViewSet):
    serializer_class = SubjectSerializer
    permission_classes = [IsAdminOrReadOnly]
    ordering_fields = ['create_date']
    ordering = ['-create_date']

    def get_queryset(self):
        user_type = self.request.auth.get('user_type')
        user_id = self.request.auth.get('user_id')
        if user_type == 'systemadmin' or user_type == 'user':
            return Subject.objects.all()
        if user_type == 'teacher':
            subject_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('subjectid', flat=True).distinct()
            return Subject.objects.filter(subjectid__in=subject_ids)
        return Subject.objects.none()