# In backend/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# --- 1. IMPORT THE DEFAULT VIEW WITH A NEW NAME ---
from rest_framework_simplejwt.views import TokenRefreshView as DefaultTokenRefreshView

# --- 2. IMPORT OUR NEW CUSTOM SERIALIZER ---
from .serializers import CustomTokenRefreshSerializer


# --- 3. CREATE A CUSTOM VIEW THAT USES OUR SERIALIZER ---
class CustomTokenRefreshView(DefaultTokenRefreshView):
    """
    This custom view uses our CustomTokenRefreshSerializer
    to refresh tokens without checking the database.
    """
    serializer_class = CustomTokenRefreshSerializer


# --- 4. ROUTER (No Change) ---
router = DefaultRouter()
router.register(r'teachers', views.TeacherViewSet, basename='teacher')
router.register(r'classes', views.ClassesViewSet, basename='class')
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'parents', views.ParentsViewSet, basename='parent')
router.register(r'systemadmins', views.SystemadminViewSet, basename='systemadmin')
router.register(r'users', views.UserViewSet, basename='user')


# --- 5. URLPATTERNS (Updated) ---
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    
    # --- 6. USE OUR NEW CUSTOM REFRESH VIEW ---
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    path('', include(router.urls)),
]