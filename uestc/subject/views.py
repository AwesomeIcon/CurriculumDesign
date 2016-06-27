from django.shortcuts import render,render_to_response

# Create your views here.


def login(request):
    return render_to_response('login.html')


def index(request):
    return render_to_response('index.html')
