from django.shortcuts import render,render_to_response
import hashlib
# Create your views here.


def login(request):
    return render_to_response('login.html')


def index(request):
    return render_to_response('index.html')


def md5(str):
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()
