from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def home(request):
    return render(request, 'homeApp/home.html', {})
