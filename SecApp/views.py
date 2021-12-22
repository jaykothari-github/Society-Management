from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *

# Create your views here.

def signin(request):
    return render(request,'sign-in.html')

def signup(request):
    return render(request,'sign-up.html')

def OTP(request):

    try:
        SecUser.objects.get(email = request.POST['email'])
        return JsonResponse({'msg':'Email is already register'})
        
    except:
        if request.POST['password'] == request.POST['cpassword']:
            pass
        else:
            return JsonResponse({'pass_msg':'Password and Confirm password are not same'})



    return JsonResponse({'res':'Rec'})