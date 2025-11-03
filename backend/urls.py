# In backend/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from rest_framework_simplejwt.views import TokenRefreshView # <-- Import this

# --- 1. Create the router ---
router = DefaultRouter()

# --- 2. Register all our ViewSets ---
router.register(r'teachers', views.TeacherViewSet, basename='teacher')
router.register(r'classes', views.ClassesViewSet, basename='class')
router.register(r'sections', views.SectionViewSet, basename='section')
router.register(r'subjects', views.SubjectViewSet, basename='subject')
router.register(r'students', views.StudentViewSet, basename='student')
# --- Add the 3 MISSING routes ---
router.register(r'parents', views.ParentsViewSet, basename='parent')
router.register(r'systemadmins', views.SystemadminViewSet, basename='systemadmin')
router.register(r'users', views.UserViewSet, basename='user')


urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    
    # Add the refresh token URL
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Include all the router URLs
    path('', include(router.urls)),
]