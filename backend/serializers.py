# In backend/serializers.py
from rest_framework import serializers
from .models import *
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

# --- 1. IMPORT OUR "CRASH-PROOF" HELPER ---
from .token_utils import get_token_claim
# ---

# --- 2. IMPORT OUR HASHING HELPER ---
from .hash_utils import make_ci_hash


# --- 1. AUDIT BASE CLASS ---
class AuditBaseSerializer(serializers.ModelSerializer):
    """
    Base serializer that automatically adds
    create_userid, create_username, and create_usertype.
    """
    def create(self, validated_data):
        # --- HARDENED ---
        # Get the request object from the context
        request = self.context.get('request')
        
        # Safely get user data using our helper
        user_id = get_token_claim(request, 'user_id', 0)
        username = get_token_claim(request, 'username', 'unknown')
        user_type = get_token_claim(request, 'user_type', 'unknown')
        
        # Add the audit fields
        validated_data['create_userid'] = user_id
        validated_data['create_username'] = username
        validated_data['create_usertype'] = user_type
        
        return super().create(validated_data)

# --- 2. "USER" BASE CLASS ---
class BaseUserSerializer(AuditBaseSerializer):
    """
    Handles password hashing and cross-table username validation.
    """
    
    def validate_username(self, value):
        model = self.Meta.model
        all_user_models = [Teacher, Student, Parents, Systemadmin, User]
        
        for user_model in all_user_models:
            query = user_model.objects.filter(username=value)
            
            if self.instance and isinstance(self.instance, user_model):
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                raise serializers.ValidationError(f"This username is already taken by a {user_model.__name__}.")
                
        return value
    
    def create(self, validated_data):
        if 'password' in validated_data:
            # Use our CodeIgniter-compatible hash function
            validated_data['password'] = make_ci_hash(validated_data['password'])
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        if 'password' in validated_data:
            # Use our CodeIgniter-compatible hash function
            validated_data['password'] = make_ci_hash(validated_data['password'])
        
        return super().update(instance, validated_data)

# --- 3. ALL USER SERIALIZERS ---
# (These now inherit the "hardened" AuditBaseSerializer)

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
    parent_name = serializers.StringRelatedField(source='parentid', read_only=True)

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
    students = StudentSerializer(many=True, read_only=True, source='student_set')
    
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
        
# --- 4. ADMIN SETUP SERIALIZERS ---
# (These inherit the "hardened" AuditBaseSerializer)

class ClassesSerializer(AuditBaseSerializer):
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

class ExamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exam
        fields = '__all__'

class GradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grade
        fields = '__all__'
        
class SubjectteacherSerializer(AuditBaseSerializer):
    class Meta:
        model = Subjectteacher
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }

class MarkpercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markpercentage
        fields = '__all__'
        
class MarkrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markrelation
        fields = '__all__'

# --- 5. "SMART" SERIALIZERS ---
# (These have their own audit fields and are now "hardened")

class MarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mark
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'create_userID': {'read_only': True},
            'create_usertypeID': {'read_only': True},
        }

    def create(self, validated_data):
        # --- HARDENED ---
        request = self.context.get('request')
        
        # Safely get user data
        user_id = get_token_claim(request, 'user_id', 0)
        user_type_str = get_token_claim(request, 'user_type')
        
        usertypeid_map = {'systemadmin': 1, 'teacher': 2}
        
        validated_data['create_date'] = timezone.now()
        validated_data['create_userID'] = user_id
        validated_data['create_usertypeID'] = usertypeid_map.get(user_type_str)

        return super().create(validated_data)

class StudentattendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'create_userID': {'read_only': True},
            'create_usertypeID': {'read_only': True},
            'year': {'read_only': True},
        }

    def create(self, validated_data):
        # --- HARDENED ---
        request = self.context.get('request')
        
        user_id = get_token_claim(request, 'user_id', 0)
        user_type_str = get_token_claim(request, 'user_type')
        usertypeid_map = {'systemadmin': 1, 'teacher': 2}
        
        validated_data['create_date'] = timezone.now()
        validated_data['create_userID'] = user_id
        validated_data['create_usertypeID'] = usertypeid_map.get(user_type_str)

        if 'monthyear' in validated_data:
            validated_data['year'] = validated_data['monthyear'][:4]

        return super().create(validated_data)

class TeacherattendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tattendance
        fields = '__all__'
        
class UserattendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Uattendance
        fields = '__all__'

class ExamattendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eattendance
        fields = '__all__'

class RoutineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Routine
        fields = '__all__'

class SyllabusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Syllabus
        fields = '__all__'
        extra_kwargs = {
            'userid': {'read_only': True},
            'usertypeid': {'read_only': True},
        }
    
    def create(self, validated_data):
        # --- HARDENED ---
        request = self.context.get('request')
        
        user_id = get_token_claim(request, 'user_id', 0)
        user_type_str = get_token_claim(request, 'user_type')
        
        usertypeid_map = {
            'systemadmin': 1, 'teacher': 2, 'student': 3,
            'parent': 4, 'staff': 5,
        }
        
        validated_data['userid'] = user_id
        validated_data['usertypeid'] = usertypeid_map.get(user_type_str)

        if 'date' not in validated_data:
            validated_data['date'] = timezone.now().date()
            
        return super().create(validated_data)

class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'
        extra_kwargs = {
            'userid': {'read_only': True},
            'usertypeid': {'read_only': True},
        }
    
    def create(self, validated_data):
        # --- HARDENED ---
        request = self.context.get('request')
        
        user_id = get_token_claim(request, 'user_id', 0)
        user_type_str = get_token_claim(request, 'user_type')
        
        usertypeid_map = {
            'systemadmin': 1, 'teacher': 2, 'student': 3,
            'parent': 4, 'staff': 5,
        }
        
        validated_data['userid'] = user_id
        validated_data['usertypeid'] = usertypeid_map.get(user_type_str)
            
        return super().create(validated_data)

class AssignmentanswerSerializer(serializers.ModelSerializer):
    student_name = serializers.SerializerMethodField()
    
    class Meta:
        model = Assignmentanswer
        fields = '__all__'
        extra_kwargs = {
            'uploaderid': {'read_only': True},
            'uploadertypeid': {'read_only': True},
            'answerdate': {'read_only': True},
        }

    def get_student_name(self, obj):
        try:
            student = Student.objects.get(studentid=obj.uploaderid)
            return student.name
        except Student.DoesNotExist:
            return "Unknown Student"

    def create(self, validated_data):
        # --- HARDENED ---
        request = self.context.get('request')
        user_type_str = get_token_claim(request, 'user_type')
        
        if request and user_type_str == 'student':
            user_id = get_token_claim(request, 'user_id', 0)
            
            validated_data['uploaderid'] = user_id
            validated_data['uploadertypeid'] = 3 # 3 = Student
            validated_data['answerdate'] = timezone.now().date()
            
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("Only students can submit answers.")
            
class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_usertypeid': {'read_only': True},
        }
    
    def create(self, validated_data):
        # --- HARDENED ---
        request = self.context.get('request')
        
        user_id = get_token_claim(request, 'user_id', 0)
        user_type_str = get_token_claim(request, 'user_type')
        
        usertypeid_map = {
            'systemadmin': 1, 'teacher': 2, 'student': 3,
            'parent': 4, 'staff': 5,
        }
        
        validated_data['create_date'] = timezone.now()
        validated_data['create_userid'] = user_id
        validated_data['create_usertypeid'] = usertypeid_map.get(user_type_str)
            
        return super().create(validated_data)


# --- 6. TOKEN REFRESH SERIALIZER ---

class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    """
    This custom serializer refreshes a token without
    checking the database (Token Blacklisting).
    """
    def validate(self, attrs):
        # This skips the database check for a blacklisted token.
        # It only validates the token's signature and expiry.
        return super(TokenRefreshSerializer, self).validate(attrs)