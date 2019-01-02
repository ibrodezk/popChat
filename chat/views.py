from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'chat/index.html', {})

def room(request, room_name):
    return render(request, 'chat/room.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })

def loginTest(request):
    # social_core.pipeline.social_auth.=
    return render(request, 'chat/loginTest.html', {})


def twitchInput(request):
    # return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/chat/'))
    return render(request, 'chat/loginTest.html', {})
