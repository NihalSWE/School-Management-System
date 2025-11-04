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
        return user_type == 'systemadmin' or user_type == 'user'

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
            return user_type == 'systemadmin' or user_type == 'user'
        
        # For 'list', 'retrieve', 'update', 'delete',
        # any authenticated user can *try*.
        # has_object_permission will do the final check.
        return True

    def has_object_permission(self, request, view, obj):
        # 'obj' is the Student object
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        # Admins can do anything to any object
        if user_type == 'systemadmin' or user_type == 'user':
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
            return user_type == 'systemadmin' or user_type == 'user'
        
        return True # Allow list, retrieve, update, delete *attempts*

    def has_object_permission(self, request, view, obj):
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        # Admins can do anything
        if user_type == 'systemadmin' or user_type == 'user':
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
            return user_type == 'systemadmin' or user_type == 'user'
        return True

    def has_object_permission(self, request, view, obj):
        user_type = request.auth.get('user_type')
        user_id = request.auth.get('user_id')

        if user_type == 'systemadmin' or user_type == 'user':
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
        return user_type == 'systemadmin' or user_type == 'user'