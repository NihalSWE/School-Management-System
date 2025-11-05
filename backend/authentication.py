# In backend/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.utils.translation import gettext_lazy as _
from rest_framework import exceptions

# Import all 5 of our user models
from .models import Teacher, Student, Parents, Systemadmin, User

class CustomJWTAuthentication(JWTAuthentication):
    """
    This is our "smart" auth class. It overrides the 'get_user'
    method to look in the correct user table based on the
    'user_type' claim we added to our token.
    """
    
    def get_user(self, validated_token):
        """
        Attempts to find a user in the database based on the 'user_type'
        and 'user_id' claims in the validated token.
        """
        try:
            user_id = validated_token.get('user_id')
            user_type = validated_token.get('user_type')

            if not user_id or not user_type:
                raise exceptions.AuthenticationFailed(_('Token is invalid or missing custom claims.'))

            # Look in the correct model based on the 'user_type' claim
            if user_type == 'teacher':
                user = Teacher.objects.get(pk=user_id)
            elif user_type == 'student':
                user = Student.objects.get(pk=user_id)
            elif user_type == 'parent':
                user = Parents.objects.get(pk=user_id)
            elif user_type == 'systemadmin':
                user = Systemadmin.objects.get(pk=user_id)
            elif user_type == 'staff':
                user = User.objects.get(pk=user_id)
            else:
                raise exceptions.AuthenticationFailed(_('Invalid user type in token.'))

            return user

        except Teacher.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Teacher not found.'))
        except Student.DoesNotExist:
            # --- THIS IS THE FIXED LINE ---
            raise exceptions.AuthenticationFailed(_('Student not found.')) 
        except Parents.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Parent not found.'))
        except Systemadmin.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('Admin not found.'))
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed(_('User not found.'))
        except Exception as e:
            # Catch all other potential errors
            raise exceptions.AuthenticationFailed(str(e))