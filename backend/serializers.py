# In backend/serializers.py
from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from .hash_utils import make_ci_hash

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
        
        # Get the current time once
        now = timezone.now()
        
        if request and request.user.is_authenticated:
            # Set all the audit fields that our models need
            validated_data['create_date'] = now
            
            # --- THIS IS THE FIX ---
            # All our audit models (Teacher, Student, Markpercentage)
            # require modify_date to be set on creation.
            validated_data['modify_date'] = now 
            
            validated_data['create_userid'] = request.auth.get('user_id')
            validated_data['create_username'] = request.user.username
            
            # This is the field your main user tables use
            validated_data['create_usertype'] = request.auth.get('user_type') 
        
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
            # --- THIS IS THE FIX ---
            # Was: make_password(validated_data['password'])
            validated_data['password'] = make_ci_hash(validated_data['password'])
        
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        # Hash password *if* it's being updated
        if 'password' in validated_data:
            # --- THIS IS THE FIX ---
            # Was: make_password(validated_data['password'])
            validated_data['password'] = make_ci_hash(validated_data['password'])
        
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



class RoutineSerializer(serializers.ModelSerializer):
    """ Serializer for the 'Routine' table. """
    class Meta:
        model = Routine
        fields = '__all__'

class SyllabusSerializer(serializers.ModelSerializer):
    """
    SPECIAL Serializer for the 'Syllabus' table.
    It manually handles its audit fields (userid, usertypeid) on creation.
    """
    class Meta:
        model = Syllabus
        fields = '__all__'
        extra_kwargs = {
            'userid': {'read_only': True},
            'usertypeid': {'read_only': True},
        }
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['userid'] = request.auth.get('user_id')
            
            # Map the string 'user_type' to the integer 'usertypeid'
            user_type_str = request.auth.get('user_type')
            usertypeid_map = {
                'systemadmin': 1,
                'teacher': 2,
                'student': 3,
                'parent': 4,
                'staff': 5,
            }
            validated_data['usertypeid'] = usertypeid_map.get(user_type_str)

        # Set date if not provided
        if 'date' not in validated_data:
            from django.utils import timezone
            validated_data['date'] = timezone.now().date()
            
        return super().create(validated_data)

class AssignmentSerializer(serializers.ModelSerializer):
    """
    SPECIAL Serializer for the 'Assignment' table.
    It manually handles its audit fields (userid, usertypeid) on creation.
    """
    class Meta:
        model = Assignment
        fields = '__all__'
        extra_kwargs = {
            'userid': {'read_only': True},
            'usertypeid': {'read_only': True},
        }
    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['userid'] = request.auth.get('user_id')
            
            # Map the string 'user_type' to the integer 'usertypeid'
            user_type_str = request.auth.get('user_type')
            usertypeid_map = {
                'systemadmin': 1,
                'teacher': 2,
                'student': 3,
                'parent': 4,
                'staff': 5,
            }
            validated_data['usertypeid'] = usertypeid_map.get(user_type_str)
            
        return super().create(validated_data)

class AssignmentanswerSerializer(serializers.ModelSerializer):
    """
    SPECIAL Serializer for the 'Assignmentanswer' table.
    It manually handles audit fields (uploaderID, uploadertypeID, answerdate)
    on creation, as it's submitted by a Student.
    """
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
        """
        This method looks up the student's name
        using the 'uploaderid' from the answer.
        """
        try:
            # Student model is already imported by StudentSerializer
            student = Student.objects.get(studentid=obj.uploaderid)
            return student.name
        except Student.DoesNotExist:
            return "Unknown Student"
    
    def create(self, validated_data):
        request = self.context.get('request')
        
        # This action MUST be done by a student
        if request and request.auth.get('user_type') == 'student':
            validated_data['uploaderid'] = request.auth.get('user_id')
            validated_data['uploadertypeid'] = 3 # 3 = Student
            
            from django.utils import timezone
            validated_data['answerdate'] = timezone.now().date()
            
            return super().create(validated_data)
        else:
            raise serializers.ValidationError("Only students can submit answers.")


# --- 5. MARKING SYSTEM "SETUP" SERIALIZERS ---

class ExamSerializer(serializers.ModelSerializer): # <-- THE FIX
    class Meta:
        model = Exam
        fields = '__all__'
       

class GradeSerializer(serializers.ModelSerializer): # <-- THE FIX
    class Meta:
        model = Grade
        fields = '__all__'
      

# --- THIS IS THE MAIN MARK SERIALIZER ---

class MarkSerializer(serializers.ModelSerializer):
    """
    This serializer creates the "Mark Header" record.
    It manually handles its own special audit fields.
    It does NOT handle the score itself.
    """
    # --- Smart Read-Only Fields (for GET requests) ---
    student_name = serializers.StringRelatedField(source='studentid', read_only=True)
    class_name = serializers.StringRelatedField(source='classesid', read_only=True)
    exam_name_from_id = serializers.StringRelatedField(source='examid', read_only=True)

    class Meta:
        model = Mark
        fields = '__all__'
        extra_kwargs = {
            # We make the audit fields read-only in the API...
            # ...because we provide them in the create() method.
            'create_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_usertypeid': {'read_only': True},
        }

    #
    # --- WE HAVE REMOVED THE _get_grade_for_mark METHOD ---
    #
    
    def create(self, validated_data):
        # --- 1. MANUALLY ADD AUDIT FIELDS (WITH MAPPING) ---
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['create_date'] = timezone.now()
            validated_data['create_userid'] = request.auth.get('user_id')
            
            # --- THIS FIXES THE "usertypeID cannot be null" ERROR ---
            user_type_str = request.auth.get('user_type') # e.g., "teacher"
            
            # Map the string name to the integer ID
            usertypeid = None
            if user_type_str == 'systemadmin':
                usertypeid = 1
            elif user_type_str == 'teacher':
                usertypeid = 2
            elif user_type_str == 'student':
                usertypeid = 3
            elif user_type_str == 'parent':
                usertypeid = 4
            elif user_type_str == 'user':
                usertypeid = 5
            
            validated_data['create_usertypeid'] = usertypeid
        
        # --- 2. WE HAVE REMOVED THE BROKEN "SMART" GRADE LOGIC ---
        
        return super().create(validated_data)
    
class MarkpercentageSerializer(AuditBaseSerializer):
    class Meta:
        model = Markpercentage
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }
    
class MarkrelationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Markrelation
        fields = '__all__'
    
class SubjectteacherSerializer(serializers.ModelSerializer): # <-- THE FIX
    # --- Smart Read-Only Fields ---
    class_name = serializers.StringRelatedField(source='classesid', read_only=True)
    section_name = serializers.StringRelatedField(source='sectionid', read_only=True)
    subject_name = serializers.StringRelatedField(source='subjectid', read_only=True)
    teacher_name = serializers.StringRelatedField(source='teacherid', read_only=True)

    class Meta:
        model = Subjectteacher
        fields = '__all__'




class StudentattendanceSerializer(serializers.ModelSerializer):
    """
    SPECIAL Serializer for the 'Attendance' (student) crosstab table.
    It manually handles its audit fields (userid, usertype) on creation.
    """
    class Meta:
        model = Attendance
        fields = '__all__'
        
        # Tell DRF that these fields are provided by the server,
        # not by the user in the POST body.
        extra_kwargs = {
            'userid': {'read_only': True},
            'usertype': {'read_only': True},
        }
    
    def create(self, validated_data):
        # Manually add the "creator" (the teacher) from the token
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['userid'] = request.auth.get('user_id')
            validated_data['usertype'] = request.auth.get('user_type')
        return super().create(validated_data)

class TeacherattendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Tattendance' (teacher) crosstab table.
    """
    class Meta:
        model = Tattendance
        fields = '__all__'

class UserattendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Uattendance' (staff/user) crosstab table.
    """
    class Meta:
        model = Uattendance
        fields = '__all__'

class ExamattendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the 'Eattendance' (exam attendance) log table.
    """
    class Meta:
        model = Eattendance
        fields = '__all__'




# --- 5. IMPORT AND ADD THE MISSING CLASS ---


class CustomTokenRefreshSerializer(TokenRefreshSerializer):
    def validate(self, attrs):
        refresh = self.token_class(attrs["refresh"])
        data = {"access": str(refresh.access_token)}
        return data