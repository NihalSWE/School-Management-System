# In backend/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# --- IMPORT THE NEW JWT VIEWS ---
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# --- Router (no change) ---
router = DefaultRouter()
router.register(r'auth-users', views.UserViewSet, basename='auth-user')
router.register(r'profiles', views.ProfileViewSet, basename='profile')

urlpatterns = [

    path('register/', views.RegisterAPIView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
   
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # Includes all URLs from the router (no change)
    path('', include(router.urls)),
]