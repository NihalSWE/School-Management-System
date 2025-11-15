# In backend/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Subjectteacher, Student, ConversationUser

# --- THIS IS THE FIX ---
# Import our new, safe helper function
from .token_utils import get_token_claim

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins (Systemadmin)
    to write (create, update, delete).
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        return user_type == 'systemadmin'

class IsAdminOrStudentOwner(BasePermission):
    """
    Custom permission for the StudentViewSet.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')

        if view.action == 'create':
            return user_type == 'systemadmin'
        
        return True # has_object_permission will do the final check

    def has_object_permission(self, request, view, obj):
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        user_id = get_token_claim(request, 'user_id', 0) # Default to 0

        if user_type == 'systemadmin':
            return True

        if user_type == 'student':
            if view.action in ['retrieve', 'update', 'partial_update']:
                return obj.studentid == user_id
            else:
                return False

        if user_type == 'teacher':
            if view.action == 'retrieve':
                class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
                return obj.classesid_id in class_ids
            else:
                return False

        return False

class IsAdminOrTeacherOwner(BasePermission):
    """
    Custom permission for the TeacherViewSet.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')

        if view.action == 'create':
            return user_type == 'systemadmin'
        
        return True

    def has_object_permission(self, request, view, obj):
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        user_id = get_token_claim(request, 'user_id', 0)

        if user_type == 'systemadmin':
            return True

        if user_type == 'teacher':
            if view.action in ['retrieve', 'update', 'partial_update']:
                return obj.teacherid == user_id
            else:
                return False

        if user_type == 'student' or user_type == 'parent':
            if view.action == 'retrieve':
                return True
            else:
                return False

        return False

class IsAdminOrParentOwner(BasePermission):
    """
    Custom permission for the ParentsViewSet.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        
        if view.action == 'create':
            return user_type == 'systemadmin'
        return True

    def has_object_permission(self, request, view, obj):
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        user_id = get_token_claim(request, 'user_id', 0)

        if user_type == 'systemadmin':
            return True

        if user_type == 'parent':
            if view.action in ['retrieve', 'update', 'partial_update']:
                return obj.parentsid == user_id
            else:
                return False
        
        return False
    
class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admins (Systemadmin)
    to access an endpoint.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        return user_type == 'systemadmin'
    
class IsAdminOrTeacherForMarks(BasePermission):
    """
    Custom permission for the MarkViewSet.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')

        if user_type == 'systemadmin':
            return True

        if user_type == 'teacher':
            return True

        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        
        if user_type == 'systemadmin':
            return True

        if user_type == 'teacher':
            if view.action in ['retrieve', 'update', 'partial_update']:
                return True
            else:
                return False

        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS

        return False

class IsAdminOrTeacherForAttendance(BasePermission):
    """
    Custom permission for Student Attendance.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')

        if user_type == 'systemadmin' or user_type == 'teacher':
            return True

        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS

        return False

class IsAdminOrTeacherSelfCreateRead(BasePermission):
    """
    Permission for Teacher Self-Attendance (Tattendance).
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        
        if user_type == 'systemadmin':
            return True

        if user_type == 'teacher':
            return request.method in SAFE_METHODS or view.action == 'create'
        
        return False

class IsAdminOrStaffSelfCreateRead(BasePermission):
    """
    Permission for Staff Self-Attendance (Uattendance).
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        
        if user_type == 'systemadmin':
            return True

        # --- THIS WAS A BUG, 'staff' IS THE CORRECT TYPE ---
        if user_type == 'staff':
            return request.method in SAFE_METHODS or view.action == 'create'
        
        return False

class IsAdminOrTeacherWriteOwner(BasePermission):
    """
    Custom permission for Syllabus and Assignment.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')

        if user_type == 'systemadmin':
            return True
        
        if user_type == 'teacher':
            return request.method in SAFE_METHODS or view.action == 'create'

        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS
        
        return False

    def has_object_permission(self, request, view, obj):
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        user_id = get_token_claim(request, 'user_id', 0)

        if user_type == 'systemadmin':
            return True
        
        if user_type == 'teacher':
            if request.method in SAFE_METHODS:
                return True
            # Check if the teacher is the owner
            # NOTE: We assume 'userid' is the creator's ID
            return obj.userid == user_id 

        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS

        return False

class IsStudentOwnerForAnswer(BasePermission):
    """
    Custom permission for Assignment Answers.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')

        if user_type == 'systemadmin':
            return True
        
        if user_type == 'student':
            return True # Can create, list, retrieve, update, delete

        if user_type == 'teacher' or user_type == 'parent':
            return request.method in SAFE_METHODS
        
        return False

    def has_object_permission(self, request, view, obj):
        # --- USE HELPER ---
        user_type = get_token_claim(request, 'user_type')
        user_id = get_token_claim(request, 'user_id', 0)

        if user_type == 'systemadmin':
            return True
        
        if user_type == 'student':
            # Student can do anything to *their own* answer
            return obj.uploaderid == user_id

        if user_type == 'teacher':
            return request.method in SAFE_METHODS

        if user_type == 'parent':
            if request.method in SAFE_METHODS:
                student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
                return obj.uploaderid in student_ids
            
        return False
    
    
class IsAdminOrTeacherWriteReadOnly(BasePermission):
    """
    "Flawless" Permission:
    - Admins and Teachers can Create, Update, Delete.
    - Students and Parents can only Read.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        user_type = get_token_claim(request, 'user_type')
        
        if user_type == 'systemadmin' or user_type == 'teacher':
            return True # Admins and Teachers can do anything
        
        # Students and Parents can only use "safe" methods (GET)
        return request.method in SAFE_METHODS
    
    
class IsAdminOrTeacherOrStudentReadOnly(BasePermission):
    """
    "Flawless" Permission for the Student list:
    - Admins can do anything.
    - Teachers can only Read.
    - Students can only Read.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        user_type = get_token_claim(request, 'user_type')
        
        if user_type == 'systemadmin':
            return True # Admins can do anything
        
        # Teachers and Students can only use "safe" methods (GET)
        if user_type == 'teacher' or user_type == 'student':
            return request.method in SAFE_METHODS
        
        return False # "Flawlessly" blocks Parents and Staff
    
    
class IsConversationParticipant(BasePermission):
    """
    SAFE & NEW:
    Permission to check if the logged-in user is part of a conversation.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        user_type = get_token_claim(request, 'user_type')
        user_id = get_token_claim(request, 'user_id', 0)
        
        # Get the conversation ID from the URL (e.g., /api/conversations/msgs/1/)
        conversation_id = view.kwargs.get('convo_id')
        
        if not conversation_id:
            # If there is no ID, it's the Inbox (list) or Compose (create) view
            return view.action in ['list', 'create']
            
        # Use your existing, working usertype names
        usertypeid_map = {
            'systemadmin': 1, 
            'teacher': 2, 
            'student': 3, 
            'parent': 4, 
            'staff': 5
        }
        user_type_id = usertypeid_map.get(user_type)
        
        if not user_type_id:
            return False # Block unknown user types

        # Check if this user is linked to this conversation
        return ConversationUser.objects.filter(
            conversation_id=conversation_id,
            user_id=user_id,
            usertypeid=user_type_id
        ).exists()
        
class IsAdminOrTeacher_Or_StudentReadOnly(BasePermission):
    """
    SAFE & CORRECTED:
    - Admins, Teachers, AND STAFF can do anything (Create, Read, Update).
    - Students (and Parents) can ONLY Read (GET).
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        user_type = get_token_claim(request, 'user_type')
        
        # --- THIS IS THE FIX ---
        # Admins, Teachers, AND Staff get full access
        if user_type == 'systemadmin' or user_type == 'teacher' or user_type == 'staff':
            return True 
        
        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS # Students/Parents can only read
            
        return False # All others blocked
    
    
class IsAdminOrTeacher(BasePermission):
    """
    SAFE & NEW:
    - Only Admins and Teachers have full access.
    - All other roles (Student, Parent, Staff) are blocked.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        user_type = get_token_claim(request, 'user_type')
        
        # This uses your existing, working 'user_type' logic
        return user_type == 'systemadmin' or user_type == 'teacher'
    
class IsStudent(BasePermission):
    """
    SAFE & NEW:
    - Only Students have access.
    - All other roles are blocked.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        user_type = get_token_claim(request, 'user_type')
        
        # This uses your existing, working 'user_type' logic
        return user_type == 'student'
    
    
class IsAdminOrStudentReadOnly(BasePermission):
    """
    SAFE & NEW:
    - Admin: Full access (GET, POST, PUT, DELETE).
    - Student: Read-Only access (GET).
    - Teacher, Parent, Staff: Blocked.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
            
        user_type = get_token_claim(request, 'user_type')
        
        if user_type == 'systemadmin':
            return True # Full access
            
        if user_type == 'student':
            return request.method in SAFE_METHODS # Read-only
            
        # Teachers, Parents, and Staff are blocked
        return False
    

class IsAdminOrOwner(BasePermission):
    """
    SAFE & NEW: "Flawless" (and 100% *Correct*) Permission.
    - Admin: Full access.
    - Authenticated User: Can create, read, update, or delete
      objects they "own" (where create_userid matches their user_id).
    """

    def has_permission(self, request, view):
        # All authenticated users (Admin, Teacher, Student) can
        # access the list (GET) or create new (POST).
        # The 'get_queryset' will handle "flawless" (and 100% *correct*) list filtering.
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # "Flawless" (and 100% *correct*) object-level security for PUT, PATCH, DELETE
        user_type = get_token_claim(request, 'user_type')
        user_id = get_token_claim(request, 'user_id', 0)

        # Admin has "flawless" (and 100% *correct*) full access
        if user_type == 'systemadmin':
            return True
        
        # "Flawless" (and 100% *correct*) check for the object's owner
        return obj.create_userid == user_id