from django.shortcuts import render
from django.http import HttpResponse

from .models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, "index.html")
def index1(request, hood):
    # return HttpResponse('Hello from Python!')
    return HttpResponse('Hello %s' % hood)
