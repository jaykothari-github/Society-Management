from django.http.response import Http404, HttpResponse
from django.shortcuts import render

# Create your views here.

def signin(request):
    return render(request,'sign-in.html')

def signup(request):
    return render(request,'sign-up.html')