# In backend/jwt_utils.py
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Teacher, Student, Parents, Systemadmin, User

def get_tokens_for_user(user):
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

    # --- ADD USER ID TO THE TOKEN ---
    refresh['user_id'] = user.pk # <-- ADD THIS
    refresh['username'] = user.username
    refresh['name'] = user.name
    
    if isinstance(user, Teacher):
        refresh['user_type'] = 'teacher'
    elif isinstance(user, Student):
        refresh['user_type'] = 'student'
    elif isinstance(user, Parents):
        refresh['user_type'] = 'parent'
    elif isinstance(user, Systemadmin):
        refresh['user_type'] = 'systemadmin'
    elif isinstance(user, User):
        refresh['user_type'] = 'staff'

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }