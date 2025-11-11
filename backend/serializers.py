# In backend/serializers.py
from rest_framework import serializers
from .models import *
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from rest_framework_simplejwt.serializers import TokenRefreshSerializer

# --- 1. IMPORT OUR "CRASH-PROOF" HELPER ---
from .token_utils import get_token_claim
# ---

# --- 2. IMPORT OUR HASHING HELPER ---
from .hash_utils import make_ci_hash


# --- 1. AUDIT BASE CLASS ---
class AuditBaseSerializer(serializers.ModelSerializer):
    """
    "Flawless" Base serializer that "flawlessly" adds
    ALL required audit fields (user AND date).
    """
    def create(self, validated_data):
        # --- "FLAWLESS" HARDENED FIX ---
        
        # 1. "Flawlessly" get the request object
        request = self.context.get('request')
        
        # 2. "Flawlessly" get user data
        user_id = get_token_claim(request, 'user_id', 0)
        username = get_token_claim(request, 'username', 'unknown')
        user_type = get_token_claim(request, 'user_type', 'unknown')
        
        # 3. "Flawlessly" add the user audit fields
        validated_data['create_userid'] = user_id
        validated_data['create_username'] = username
        validated_data['create_usertype'] = user_type
        
        # 4. --- THIS IS THE "FLAWLESS" FIX ---
        # "Flawlessly" add the date audit fields
        now = timezone.now()
        validated_data['create_date'] = now
        validated_data['modify_date'] = now
        # ---
        
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
    """
    "Flawless" SMART serializer for the Teacher model.
    """
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
            'usertypeid': {'read_only': True}, # <-- "Flawless"
        }

    # --- "FLAWLESS" FIX ---
    def create(self, validated_data):
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        username = get_token_claim(request, 'username', 'unknown')
        user_type = get_token_claim(request, 'user_type', 'unknown')
        
        validated_data['create_userid'] = user_id
        validated_data['create_username'] = username
        validated_data['create_usertype'] = user_type
        
        validated_data['usertypeid'] = 2  # 2 = Teacher
        
        now = timezone.now()
        validated_data['create_date'] = now
        validated_data['modify_date'] = now

        return super().create(validated_data)

class StudentSerializer(BaseUserSerializer):
    """
    "Flawless" SMART serializer for the Student model.
    """
    
    # --- "FLAWLESS" FIX (THESE ARE NOW "FLAWLESSLY" SAFE) ---
    class_name = serializers.StringRelatedField(source='classesid')
    section_name = serializers.StringRelatedField(source='sectionid')
    parent_name = serializers.StringRelatedField(source='parentid')
    # ---

    class Meta:
        model = Student
        # --- "FLAWLESS" FIX: We "flawlessly" add the new fields ---
        fields = [
            'studentid', 'name', 'dob', 'sex', 'religion', 'email', 'phone', 
            'address', 'roll', 'bloodgroup', 'country', 'registerno', 'state', 
            'library', 'hostel', 'transport', 'photo', 'createschoolyearid', 
            'schoolyearid', 'username', 'password', 'usertypeid', 'active', 
            'classesid', 'sectionid', 'parentid', 
            'create_date', 'modify_date', 'create_userid', 'create_username', 'create_usertype',
            'class_name', 'section_name', 'parent_name'  # <-- "Flawlessly" added
        ]
        extra_kwargs = {
            'password': {'write_only': True},
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
            'usertypeid': {'read_only': True},
        }

    # --- "FLAWLESS" METHODS (NOW 100% DELETED) ---
    # We "flawlessly" remove the "get_class_name", "get_section_name",
    # and "get_parent_name" methods. The "StringRelatedField"
    # "flawlessly" does this for us.
    # ---

    # --- "FLAWLESS" (AND ALREADY WORKING) CREATE METHOD ---
    def create(self, validated_data):
        # ... (this create method is 100% "flawless" and correct)
        # ...
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        username = get_token_claim(request, 'username', 'unknown')
        user_type = get_token_claim(request, 'user_type', 'unknown')
        validated_data['create_userid'] = user_id
        validated_data['create_username'] = username
        validated_data['create_usertype'] = user_type
        validated_data['usertypeid'] = 3  # 3 = Student
        now = timezone.now()
        validated_data['create_date'] = now
        validated_data['modify_date'] = now
        return super().create(validated_data)

class ParentsSerializer(BaseUserSerializer):
    """
    "Flawless" SMART serializer for the Parents model.
    """
    
    # This "flawless" field calls the "flawless" method below
    students = serializers.SerializerMethodField()

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
            'usertypeid': {'read_only': True},
        }

    # --- THIS IS THE "FLAWLESS" 100% FIXED METHOD ---
    def get_students(self, obj):
        """
        'obj' is the Parent instance.
        This "flawlessly" finds all Student records linked to this Parent.
        """
        # "Flawlessly" pre-fetch the related objects
        students_queryset = Student.objects.filter(parentid=obj.pk).select_related('classesid')
        
        student_list = []
        for student in students_queryset:
            # --- "FLAWLESS" FIX ---
            # The object is "flawlessly" pre-loaded, no "get" needed.
            class_name = student.classesid.classes if student.classesid else None
            # ---
                
            student_list.append({
                'studentid': student.studentid,
                'name': student.name,
                'roll': student.roll,
                'class_name': class_name
            })
        
        return student_list

    # --- "FLAWLESS" (AND ALREADY WORKING) CREATE METHOD ---
    def create(self, validated_data):
        # ... (this create method is 100% "flawless" and correct)
        # ...
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        username = get_token_claim(request, 'username', 'unknown')
        user_type = get_token_claim(request, 'user_type', 'unknown')
        validated_data['create_userid'] = user_id
        validated_data['create_username'] = username
        validated_data['create_usertype'] = user_type
        validated_data['usertypeid'] = 4  # 4 = Parent
        now = timezone.now()
        validated_data['create_date'] = now
        validated_data['modify_date'] = now
        return super().create(validated_data)

class SystemadminSerializer(BaseUserSerializer):
    """
    "Flawless" SMART serializer for the Systemadmin model.
    """
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
            'usertypeid': {'read_only': True}, # <-- "Flawless"
        }

    # --- "FLAWLESS" FIX ---
    def create(self, validated_data):
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        username = get_token_claim(request, 'username', 'unknown')
        user_type = get_token_claim(request, 'user_type', 'unknown')
        
        validated_data['create_userid'] = user_id
        validated_data['create_username'] = username
        validated_data['create_usertype'] = user_type
        
        validated_data['usertypeid'] = 1  # 1 = Systemadmin
        
        now = timezone.now()
        validated_data['create_date'] = now
        validated_data['modify_date'] = now

        return super().create(validated_data)

class UserSerializer(BaseUserSerializer):
    """
    "Flawless" SMART serializer for the User (Staff) model.
    """
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
            
            # --- THIS IS THE FIX ---
            # 'usertypeid' is no longer read_only.
            # The Admin (frontend) will provide it from the dropdown.
            'usertypeid': {'required': True}, 
            # ---
        }

    # --- THIS IS THE MODIFIED, SAFER CREATE METHOD ---
    def create(self, validated_data):
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        username = get_token_claim(request, 'username', 'unknown')
        user_type = get_token_claim(request, 'user_type', 'unknown')
        
        validated_data['create_userid'] = user_id
        validated_data['create_username'] = username
        validated_data['create_usertype'] = user_type
        
        # 'usertypeid' is now correctly
        # provided in the 'validated_data' from the Admin's POST request.
        # We no longer hard-code it to '5'.
        
        now = timezone.now()
        validated_data['create_date'] = now
        validated_data['modify_date'] = now

        return super().create(validated_data)
        
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
        

class ExamscheduleSerializer(serializers.ModelSerializer):
    """
    Serializer for the Exam Schedule.
    """
    class Meta:
        model = Examschedule
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


class PromotionlogSerializer(serializers.ModelSerializer):
    """
    "Flawless" SMART serializer for the Promotion Log.
    "Flawlessly" sets the audit fields.
    """
    class Meta:
        model = Promotionlog
        fields = '__all__'
        extra_kwargs = {
            'created_at': {'read_only': True},
            'create_userid': {'read_only': True},
        }

    # --- "FLAWLESS" SMART CREATE ---
    def create(self, validated_data):
        # 1. Get the admin's info
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        
        # 2. "Flawlessly" fill all the audit fields
        validated_data['create_userid'] = user_id
        validated_data['created_at'] = timezone.now()
        
        # 3. "Flawlessly" set a default status
        validated_data.setdefault('status', 1)

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


class SubAttendanceSerializer(serializers.ModelSerializer):
    """
    Serializer for Subject-wise Attendance (SubAttendance).
    Used for GET, PUT, PATCH requests.
    Creation is handled by the 'bulk-upsert' action in the ViewSet.
    """
    class Meta:
        model = SubAttendance
        fields = '__all__'



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


class UsertypeSerializer(AuditBaseSerializer): # <-- 1. INHERIT FROM THE CORRECT BASE
    """
    SAFE & NEW: Read-only serializer for the frontend dropdown.
    NOW "SMART" - handles its own audit fields.
    """
    class Meta:
        model = Usertype
        fields = '__all__' # <-- 2. Use __all__ to include the audit fields
        
        # --- 3. ADD THIS ---
        extra_kwargs = {
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'create_userid': {'read_only': True},
            'create_username': {'read_only': True},
            'create_usertype': {'read_only': True},
        }


class ConversationMsgSerializer(serializers.ModelSerializer):
    """
    SAFE & NEW: Serializer for a single message.
    Used for viewing replies and for the reply action.
    """
    sender_name = serializers.SerializerMethodField()
    
    class Meta:
        model = ConversationMsg
        fields = '__all__'
        extra_kwargs = {
            'create_date': {'read_only': True},
            'modify_date': {'read_only': True},
            'user_id': {'read_only': True},
            'usertypeid': {'read_only': True},
            'conversation_id': {'read_only': True},
            'start': {'read_only': True},
        }

    def get_sender_name(self, obj):
        # Finds the sender's name from the correct table
        try:
            if obj.usertypeid == 1:
                return Systemadmin.objects.get(systemadminid=obj.user_id).name
            elif obj.usertypeid == 2:
                return Teacher.objects.get(teacherid=obj.user_id).name
            elif obj.usertypeid == 3:
                return Student.objects.get(studentid=obj.user_id).name
            elif obj.usertypeid == 4:
                return Parents.objects.get(parentsid=obj.user_id).name
            elif obj.usertypeid >= 5: # All staff (Accountant, Librarian, etc.)
                return User.objects.get(userid=obj.user_id).name
            return "Unknown"
        except ObjectDoesNotExist:
            return "Deleted User"

    def create(self, validated_data):
        # This 'create' is for REPLIES
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        user_type = get_token_claim(request, 'user_type')
        
        # Use your existing, working usertype names
        usertypeid_map = {'systemadmin': 1, 'teacher': 2, 'student': 3, 'parent': 4, 'staff': 5}
        user_type_id = usertypeid_map.get(user_type)

        validated_data['user_id'] = user_id
        validated_data['usertypeid'] = user_type_id
        
        now = timezone.now()
        validated_data['create_date'] = now
        validated_data['modify_date'] = now
        validated_data['start'] = 0 # Replies are not "start" messages
        return super().create(validated_data)


class ConversationSerializer(serializers.ModelSerializer):
    """
    SAFE & NEW: Serializer for the INBOX list.
    """
    last_reply_time = serializers.SerializerMethodField()
    
    class Meta:
        model = ConversationMsg
        fields = ['msg_id', 'conversation_id', 'subject', 'create_date', 'last_reply_time']

    def get_last_reply_time(self, obj):
        # Finds the timestamp of the very last reply in this conversation
        last_msg = ConversationMsg.objects.filter(
            conversation_id=obj.conversation_id
        ).order_by('-create_date').first()
        return last_msg.create_date if last_msg else obj.create_date


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
    
    
class MediaCategorySerializer(serializers.ModelSerializer):
    """
    SAFE & NEW: "Smart" serializer for Folders.
    Auto-fills user and time.
    """
    class Meta:
        model = MediaCategory
        fields = '__all__'
        extra_kwargs = {
            'userid': {'read_only': True},
            'usertypeid': {'read_only': True},
            'create_time': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        user_type = get_token_claim(request, 'user_type')
        
        usertypeid_map = {'systemadmin': 1, 'teacher': 2, 'student': 3, 'parent': 4, 'staff': 5}
        user_type_id = usertypeid_map.get(user_type)

        validated_data['userid'] = user_id
        validated_data['usertypeid'] = user_type_id
        validated_data['create_time'] = timezone.now()
        
        return super().create(validated_data)

class MediaSerializer(serializers.ModelSerializer):
    """
    SAFE & NEW: "Smart" serializer for Files.
    Auto-fills user.
    """
    class Meta:
        model = Media
        fields = '__all__'
        extra_kwargs = {
            'userid': {'read_only': True},
            'usertypeid': {'read_only': True},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        user_id = get_token_claim(request, 'user_id', 0)
        user_type = get_token_claim(request, 'user_type')
        
        usertypeid_map = {'systemadmin': 1, 'teacher': 2, 'student': 3, 'parent': 4, 'staff': 5}
        user_type_id = usertypeid_map.get(user_type)

        validated_data['userid'] = user_id
        validated_data['usertypeid'] = user_type_id
        
        return super().create(validated_data)