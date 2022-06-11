import random

from django.shortcuts import redirect, render

def index(request):
    return render(request, 'index.html')

def clear(request):
    for key in list(request.session.keys()):
        del request.session[key]
    return redirect('/')


