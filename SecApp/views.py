from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange, choices


# Create your views here.

def signin(request):
    try: 
        uid = SecUser.objects.get(email=request.session['email'])
        return  render(request,'index.html')
    except:
        if request.method == 'POST':
            try:
                uid = SecUser.objects.get(email=request.POST['email'])
                if uid.password == request.POST['password']:
                    request.session['email'] = request.POST['email']
                    return render(request,'index.html',{'uid':uid})
                msg = 'Password is incorrect'
                return render(request,'sign-in.html',{'msg':msg})
            except:
                msg = 'Email is not register'
                return render(request,'sign-in.html',{'msg':msg})

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

def logout(request):
    del request.session['email']
    return redirect('sign-in')

def forgot_password(request):
    if request.method == 'POST':
        try:
            uid = SecUser.objects.get(email=request.POST['email'])
            s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@.1234567890'
            password = ''.join(choices(s,k=8))
            uid.password = password
            uid.save()
            subject = 'Welcome to Society Management App'
            message = f"""Hello {request.POST["email"]}, 
            Your new password is {password}. 
            Keep it secret and please change it after login."""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )
            return JsonResponse({'sent':'Sent success'})
        except:
            return JsonResponse('Nothing',safe=False)
    return render(request,'forgot-password.html')


def index(request):
    try:
        uid = SecUser.objects.get(email=request.session['email'])
        return render(request,'index.html',{'uid':uid})

    except:
        return render(request,'sign-in.html',{'msg':"session has been expired"})

def profile(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
        uid.name = request.POST['name']
        uid.mobile = request.POST['mobile']
        if 'pic' in request.FILES:
            uid.pic = request.FILES['pic']
        uid.save()
        return render(request,'profile.html',{'uid':uid,'msg':'Profile Updated'})
    return render(request,'profile.html',{'uid':uid})