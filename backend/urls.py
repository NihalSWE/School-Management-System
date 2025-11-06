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
router.register(r'routines', views.RoutineViewSet, basename='routine')
router.register(r'syllabuses', views.SyllabusViewSet, basename='syllabus')
router.register(r'assignments', views.AssignmentViewSet, basename='assignment')
router.register(r'assignmentanswers', views.AssignmentanswerViewSet, basename='assignmentanswer')
router.register(r'students', views.StudentViewSet, basename='student')
router.register(r'parents', views.ParentsViewSet, basename='parent')
router.register(r'systemadmins', views.SystemadminViewSet, basename='systemadmin')
router.register(r'users', views.UserViewSet, basename='user')
router.register(r'exams', views.ExamViewSet, basename='exam')
router.register(r'grades', views.GradeViewSet, basename='grade')
router.register(r'marks', views.MarkViewSet, basename='mark')
router.register(r'markrelations', views.MarkrelationViewSet, basename='markrelation')
router.register(r'markpercentages', views.MarkpercentageViewSet, basename='markpercentage')
router.register(r'subjectteachers', views.SubjectteacherViewSet, basename='subjectteacher')
router.register(r'studentattendance', views.StudentattendanceViewSet, basename='studentattendance')
router.register(r'teacherattendance', views.TeacherattendanceViewSet, basename='teacherattendance')
router.register(r'userattendance', views.UserattendanceViewSet, basename='userattendance')
router.register(r'examattendance', views.ExamattendanceViewSet, basename='examattendance')


# --- 5. URLPATTERNS (Updated) ---
urlpatterns = [
    path('login/', views.CustomLoginView.as_view(), name='custom_login'),
    
    # --- 6. USE OUR NEW CUSTOM REFRESH VIEW ---
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    
    path('', include(router.urls)),
]