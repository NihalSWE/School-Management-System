# In backend/urls.py (the new file you just created)

from django.urls import path
from . import views  # This imports your views.py file

urlpatterns = [
    # This says: when someone visits 'designations/',
    # run the 'get_designations' view.
    path('designations/', views.get_designations, name='get-designations'),
]