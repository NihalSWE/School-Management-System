# In backend/serializers.py
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.utils import timezone # <-- We fixed this

# --- HELPER METHOD TO GET USER INFO FROM TOKEN ---
def get_user_info_from_request(request):
    if request and hasattr(request, 'user') and request.user.is_authenticated:
        try:
            token = request.auth
            return {
                'user_id': token.get('user_id'),
                'username': token.get('username'),
                'user_type_name': token.get('user_type')
            }
        except Exception:
            return { 'user_id': 0, 'username': 'unknown', 'user_type_name': 'unknown' }
    return { 'user_id': 0, 'username': 'anonymous', 'user_type_name': 'anonymous' }


# --- 1. NEW "AUDIT" BASE CLASS ---
# This single class will auto-fill create/modify fields
# for ALL models that need it.
class AuditBaseSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        request = self.context.get('request')
        user_info = get_user_info_from_request(request)

        # Auto-fill the audit fields
        validated_data['create_date'] = timezone.now()
        validated_data['modify_date'] = timezone.now()
        validated_data['create_userid'] = user_info.get('user_id', 0)
        validated_data['create_username'] = user_info.get('username', 'unknown')
        validated_data['create_usertype'] = user_info.get('user_type_name', 'unknown')
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Automatically update the modify_date on every PUT/PATCH
        validated_data['modify_date'] = timezone.now()
        return super().update(instance, validated_data)

# --- 2. UPDATE "USER" BASE CLASS ---
# It now inherits from our new AuditBaseSerializer
class BaseUserSerializer(AuditBaseSerializer):
    def create(self, validated_data):
        # Hash password if it exists
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        # The parent (AuditBaseSerializer) will handle the audit fields
        return super().create(validated_data)

# --- 3. ALL SERIALIZERS ARE NOW CLEANER ---

class TeacherSerializer(BaseUserSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            # Set all auto-filled fields to read_only
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }

class StudentSerializer(BaseUserSerializer):
    class_name = serializers.StringRelatedField(source='classesid', read_only=True)
    section_name = serializers.StringRelatedField(source='sectionid', read_only=True)
    class Meta:
        model = Student
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }

class ParentsSerializer(BaseUserSerializer):
    class Meta:
        model = Parents
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }

class SystemadminSerializer(BaseUserSerializer):
    class Meta:
        model = Systemadmin
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }

class UserSerializer(BaseUserSerializer):
    class Meta:
        model = User
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }

# --- 4. UPDATE "LOOKUP" SERIALIZERS ---
# They now inherit from AuditBaseSerializer and will auto-fill!

class ClassesSerializer(AuditBaseSerializer):
    teacher_name = serializers.StringRelatedField(source='teacherid', read_only=True)
    class Meta:
        model = Classes
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }

class SectionSerializer(AuditBaseSerializer):
    class_name = serializers.StringRelatedField(source='classesid', read_only=True)
    teacher_name = serializers.StringRelatedField(source='teacherid', read_only=True)
    class Meta:
        model = Section
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }

class SubjectSerializer(AuditBaseSerializer):
    class_name = serializers.StringRelatedField(source='classesid', read_only=True)
    class Meta:
        model = Subject
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }