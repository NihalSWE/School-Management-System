from django.shortcuts import render
# In backend/views.py

from django.http import JsonResponse
from .models import Designations

def get_designations(request):
    """
    This view will get all objects from the Designations table
    and return them as a JSON list.
    """
    # 1. Get all objects from the model
    #    (This is the main test!)
    data = Designations.objects.all()

    # 2. Convert the objects into a list of dictionaries
    #    (The .values() method is a fast way to do this)
    payload = list(data.values())

    # 3. Return the list as a JSON response
    #    (safe=False is needed to allow returning a list)
    return JsonResponse(payload, safe=False)
