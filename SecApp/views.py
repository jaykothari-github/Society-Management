from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange


# Create your views here.

def signin(request):
    return render(request,'sign-in.html')

def signup(request):
    if request.method == 'POST':
        if str(OTP_num) == request.POST['otp']:
            try:
                SecUser.objects.create(
                    name = request.POST['name'],
                    email = request.POST['email'],
                    mobile = request.POST['mobile'],
                    password = request.POST['password']
                )
                return render(request,'sign-in.html',{'msg':'Account Created Successfully'})
            except:
                return render(request,'sign-in.html',{'msg':'Something went wrong'})
                
        return render(request,'sign-up.html',{'msg':'Invalid OTP'})
    return render(request,'sign-up.html')

def OTP(request):
    if request.POST['email']:
        try:
            SecUser.objects.get(email = request.POST['email'])
            return JsonResponse({'msg':'Email is already register'})
            
        except:
            if len(request.POST['password']) >= 8:
                if request.POST['password'] == request.POST['cpassword']:
                    global OTP_num
                    OTP_num = randrange(1000,9999)
                    subject = 'Welcome to Society Management App'
                    message = f"""Hello {request.POST["email"]}, 
                    Your OTP for registration is {OTP_num}. 
                    Hope you will enjoy App."""
                    email_from = settings.EMAIL_HOST_USER
                    recipient_list = [request.POST['email'], ]
                    send_mail( subject, message, email_from, recipient_list )
                    return JsonResponse({'otp':'OTP sent on your email'})
                else:
                    return JsonResponse({'pass_msg':'Password and Confirm password are not same'})
            else:
                return JsonResponse({'pass_msg':'Password Length should be 8 char'})

    else:
        return JsonResponse({'msg':'Please Enter a valid Email'})
