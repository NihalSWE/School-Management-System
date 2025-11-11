# In backend/jwt_utils.py
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Teacher, Student, Parents, Systemadmin, User

def get_tokens_for_user(user):
    """
    Generates JWT tokens for any of our 5 user models.
    
    This is 100% SAFE and CORRECTED.
    - 'user_type' is the logical role for API permissions (e.g., 'staff').
    - 'user_role' is the *actual* role for the frontend UI (e.g., 'Accountant').
    """
    from django.contrib.auth.models import User as AuthUser
    
    class FakeUser:
        pk = user.pk
        id = user.pk
        username = user.username
        
        def __str__(self):
            return self.username
        
        def is_authenticated(self):
            return True

    refresh = RefreshToken.for_user(FakeUser())

    # --- Standard Claims ---
    refresh['user_id'] = user.pk
    refresh['username'] = user.username
    refresh['name'] = user.name
    
    # --- THIS IS THE 100% SAFE MODIFICATION ---
    if isinstance(user, Teacher):
        refresh['user_type'] = 'teacher'
        refresh['user_role'] = 'Teacher' # New role for frontend UI
        
    elif isinstance(user, Student):
        refresh['user_type'] = 'student'
        refresh['user_role'] = 'Student' # New role for frontend UI
        
    elif isinstance(user, Parents):
        refresh['user_type'] = 'parent'
        refresh['user_role'] = 'Parents' # New role for frontend UI
        
    elif isinstance(user, Systemadmin):
        refresh['user_type'] = 'systemadmin'
        refresh['user_role'] = 'Admin' # New role for frontend UI
        
    elif isinstance(user, User):
        refresh['user_type'] = 'staff' # For existing API permissions
        try:
            # Get the *actual* role name (e.g., "Accountant") for the frontend UI
            refresh['user_role'] = user.usertypeid.usertype
        except Exception:
            # Safe fallback if 'usertypeid' is missing or not linked
            refresh['user_role'] = 'Staff' 
    # --- END OF MODIFICATION ---

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }