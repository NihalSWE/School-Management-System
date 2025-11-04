# In backend/serializers.py
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.utils import timezone

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
class BaseUserSerializer(AuditBaseSerializer):
    
    # --- THIS IS THE NEW, CORRECTED VALIDATION ---
    def validate_username(self, value):
        """
        Check that the username is unique across all 5 user tables.
        """
        model = self.Meta.model
        all_user_models = [Teacher, Student, Parents, Systemadmin, User]
        
        for user_model in all_user_models:
            query = user_model.objects.filter(username=value)
            
            # If we are *updating* a user, we must exclude their
            # own record from the uniqueness check.
            if self.instance and isinstance(self.instance, user_model):
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise serializers.ValidationError(f"This username is already taken by a {user_model.__name__}.")
                
        return value
    
    def create(self, validated_data):
        # Hash password if it exists
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        # The parent (AuditBaseSerializer) will handle the audit fields
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Hash password *if* it's being updated
        if 'password' in validated_data:
            validated_data['password'] = make_password(validated_data['password'])
        
        # This now correctly ignores the password if it's not sent,
        # and the original hash will be safe.
        return super().update(instance, validated_data)

# --- 3. ALL USER SERIALIZERS ---

class TeacherSerializer(BaseUserSerializer):
    class Meta:
        model = Teacher
        fields = '__all__'
        extra_kwargs = {
            'password': {'write_only': True},
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

# --- 4. "LOOKUP" SERIALIZERS ---

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

# --- 5. IMPORT AND ADD THE MISSING CLASS ---
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        data = {"access": str(refresh.access_token)}
        return data