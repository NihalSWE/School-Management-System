# In backend/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Subjectteacher

class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins (Systemadmin or User)
    to write (create, update, delete).
    All other authenticated users (Teacher, Student) can only read.
    """

    def has_permission(self, request, view):
        # Allow read-only requests (GET, HEAD, OPTIONS) for any
        # authenticated user.
        if request.method in SAFE_METHODS:
            return True
        
        # Write permissions are only allowed if the user is an admin.
        # We check the 'user_type' claim from our custom token.
        user_type = request.auth.get('user_type')
        return user_type == 'systemadmin' 

class IsAdminOrStudentOwner(BasePermission):
    """
    Custom permission for the StudentViewSet.
    - Admins can do anything.
    - Students can read/update their OWN profile.
    - Students CANNOT delete their profile or create new students.
    - Teachers can view students in their classes.
    """

    def has_permission(self, request, view):
        # Must be authenticated to do anything
        if not (request.user and request.user.is_authenticated):
            return False

        user_type = request.auth.get('user_type')

        if view.action == 'create':
            # Only Admins can create new students
            return user_type == 'systemadmin' 
        
        # For 'list', 'retrieve', 'update', 'delete',
        # any authenticated user can *try*.
        # has_object_permission will do the final check.
        return True

    def has_object_permission(self, request, view, obj):
        # 'obj' is the Student object
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        # Admins can do anything to any object
        if user_type == 'systemadmin':
            return True

        # --- Student Rules ---
        if user_type == 'student':
            if view.action in ['retrieve', 'update', 'partial_update']:
                # Student can view or update their OWN profile
                return obj.studentid == user_id
            else:
                # Student CANNOT delete or do anything else
                return False

        # --- Teacher Rules ---
        if user_type == 'teacher':
            if view.action == 'retrieve':
                # Teacher can view students in their classes
                class_ids = Subjectteacher.objects.filter(teacherid=user_id).values_list('classesid', flat=True).distinct()
                return obj.classesid_id in class_ids
            else:
                # Teacher CANNOT update or delete students
                return False

        # Other roles (like Parent) can't do anything yet
        return False
    
# In backend/permissions.py
# ... (your IsAdminOrReadOnly and IsAdminOrStudentOwner classes are above) ...

class IsAdminOrTeacherOwner(BasePermission):
    """
    Custom permission for the TeacherViewSet.
    - Admins can do anything.
    - Teachers can read/update their OWN profile.
    - Teachers CANNOT delete their profile or create new teachers.
    - Other roles (Student, Parent) can view teacher profiles.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        user_type = request.auth.get('user_type')

        if view.action == 'create':
            # Only Admins can create new teachers
            return user_type == 'systemadmin'
        
        return True # Allow list, retrieve, update, delete *attempts*

    def has_object_permission(self, request, view, obj):
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        # Admins can do anything
        if user_type == 'systemadmin' :
            return True

        # --- Teacher Rules ---
        if user_type == 'teacher':
            if view.action in ['retrieve', 'update', 'partial_update']:
                # Teacher can view or update their OWN profile
                return obj.teacherid == user_id
            else:
                # Teacher CANNOT delete or do anything else
                return False

        # --- Student/Parent Rules ---
        if user_type == 'student' or user_type == 'parent':
            if view.action == 'retrieve':
                # Other users can VIEW teacher profiles
                return True
            else:
                # But they cannot edit/delete them
                return False

        return False

class IsAdminOrParentOwner(BasePermission):
    """
    Custom permission for the ParentsViewSet.
    - Admins can do anything.
    - Parents can read/update their OWN profile.
    - Parents CANNOT delete or create.
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        user_type = request.auth.get('user_type')
        if view.action == 'create':
            return user_type == 'systemadmin' 
        return True

    def has_object_permission(self, request, view, obj):
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        if user_type == 'systemadmin' :
            return True

        if user_type == 'parent':
            if view.action in ['retrieve', 'update', 'partial_update']:
                return obj.parentsid == user_id
            else:
                return False
        
        # Teachers/Students should not be able to edit Parents
        return False
    
class IsAdminUser(BasePermission):
    """
    Custom permission to only allow admins (Systemadmin or User)
    to access an endpoint.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        user_type = request.auth.get('user_type')
        return user_type == 'systemadmin' 
    
class IsAdminOrTeacherForMarks(BasePermission):
    """
    Custom permission for the MarkViewSet.
    - Admins can do anything.
    - Teachers can create, read, and update marks.
    - Students and Parents can only read.
    """

    def has_permission(self, request, view):
        # Must be authenticated to do anything
        if not (request.user and request.user.is_authenticated):
            return False

        user_type = request.auth.get('user_type')

        # Admins can do anything
        if user_type == 'systemadmin' :
            return True

        # Teachers can create, list, and retrieve
        if user_type == 'teacher':
            return True

        # Students and Parents can only perform read-only actions
        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS

        return False

    def has_object_permission(self, request, view, obj):
        # 'obj' is the Mark object
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        # Admins can do anything to any object
        if user_type == 'systemadmin' :
            return True

        # --- Teacher Rules ---
        if user_type == 'teacher':
            # Teachers can update or view marks
            if view.action in ['retrieve', 'update', 'partial_update']:
                # (We could add a check here to ensure it's their own student)
                return True
            else:
                return False

        # --- Student/Parent Rules ---
        if user_type == 'student' or user_type == 'parent':
            # Students/Parents can only read, not update/delete
            return request.method in SAFE_METHODS

        return False
    

class IsAdminOrTeacherForAttendance(BasePermission):
    """
    Custom permission for Student Attendance.
    - Admins can do anything.
    - Teachers can create, read, and update attendance.
    - Students and Parents can only read.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        user_type = request.auth.get('user_type')

        if user_type == 'systemadmin' or user_type == 'teacher':
            return True

        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS

        return False # 'staff' and others are blocked

class IsAdminOrTeacherSelfCreateRead(BasePermission):
    """
    Permission for Teacher Self-Attendance (Tattendance).
    - Admin can do anything.
    - Teacher can CREATE and READ their OWN records.
    - Teacher CANNOT update or delete.
    """
    def has_permission(self, request, view):
        user_type = request.auth.get('user_type')
        if user_type == 'systemadmin':
            return True # Admin can do all actions

        if user_type == 'teacher':
            # Allow READ (GET, HEAD, OPTIONS) and CREATE (POST)
            return request.method in SAFE_METHODS or view.action == 'create'
        
        return False # Block everyone else

class IsAdminOrStaffSelfCreateRead(BasePermission):
    """
    Permission for Staff Self-Attendance (Uattendance).
    - Admin can do anything.
    - Staff can CREATE and READ their OWN records.
    - Staff CANNOT update or delete.
    """
    def has_permission(self, request, view):
        user_type = request.auth.get('user_type')
        if user_type == 'systemadmin':
            return True # Admin can do all actions

        if user_type == 'staff':
            # Allow READ (GET, HEAD, OPTIONS) and CREATE (POST)
            return request.method in SAFE_METHODS or view.action == 'create'
        
        return False # Block everyone else
    
    
class IsAdminOrTeacherWriteOwner(BasePermission):
    """
    Custom permission for Syllabus and Assignment.
    - Admins can do anything.
    - Teachers can CREATE, READ, and UPDATE/DELETE *their own* entries.
    - Students and Parents can only READ.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        user_type = request.auth.get('user_type')

        # Admins can do anything
        if user_type == 'systemadmin':
            return True
        
        # Teachers can create and read
        if user_type == 'teacher':
            return request.method in SAFE_METHODS or view.action == 'create'

        # Students/Parents can only read
        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS
        
        return False # Block 'staff'

    def has_object_permission(self, request, view, obj):
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        # Admins can do anything
        if user_type == 'systemadmin':
            return True
        
        # Teachers can read, update, or delete *their own* records
        if user_type == 'teacher':
            if request.method in SAFE_METHODS:
                return True # Allow reading
            # Check if the teacher is the owner of the object
            return obj.userid == user_id 

        # Students/Parents can only read
        if user_type == 'student' or user_type == 'parent':
            return request.method in SAFE_METHODS

        return False
    
class IsStudentOwnerForAnswer(BasePermission):
    """
    Custom permission for Assignment Answers.
    - Students can CREATE answers, and READ/UPDATE/DELETE *their own*.
    - Teachers can READ all answers for assignments in their class.
    - Admins can do anything.
    - Parents can READ their child's answers.
    """
    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False
        
        user_type = request.auth.get('user_type')

        # Admins can do anything
        if user_type == 'systemadmin':
            return True
        
        # Students can create and read
        if user_type == 'student':
            return True

        # Teachers and Parents can read
        if user_type == 'teacher' or user_type == 'parent':
            return request.method in SAFE_METHODS
        
        return False

    def has_object_permission(self, request, view, obj):
        # 'obj' is the Assignmentanswer
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        # Admins can do anything
        if user_type == 'systemadmin':
            return True
        
        # Students can read, update, or delete *their own* answer
        if user_type == 'student':
            return obj.uploaderid == user_id

        # Teachers can read any answer
        if user_type == 'teacher':
            return request.method in SAFE_METHODS

        # Parents can read their child's answer
        if user_type == 'parent':
            if request.method in SAFE_METHODS:
                from .models import Student # Local import
                student_ids = Student.objects.filter(parentid=user_id).values_list('studentid', flat=True)
                return obj.uploaderid in student_ids
            
        return False