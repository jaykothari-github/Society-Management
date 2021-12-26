from django.db.models.manager import EmptyManager
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange, choices
from MemberApp import models as mm


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

def change_password(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.method == 'POST':
        if request.POST['oldpass'] == uid.password:
            if len(request.POST['password']) > 7:
                if request.POST['password'] == request.POST['cpassword']:
                    uid.password = request.POST['password']
                    uid.save()
                    return render(request,'change-password.html',{'msg':'Password has been updated','uid':uid})
                return render(request,'change-password.html',{'msg':'Password and Confirm Password are not same','uid':uid})
            return render(request,'change-password.html',{'uid':uid,'msg':'Password Length should be atleast 8'})
        return render(request,'change-password.html',{'uid':uid,'msg':'Old Password is incorrect'})
    return render(request,'change-password.html',{'uid':uid})

def emergency(request):
    uid = SecUser.objects.get(email = request.session['email'])
    contacts = Emergency.objects.all()[::-1]
    if request.method == 'POST':
        Emergency.objects.create(
            uid= uid,
            name=request.POST['name'],
            mobile = request.POST['mobile'],
            email = request.POST['email'],
            occupation = request.POST['occupation'],
            des = request.POST['des']
        )
        return render(request,'emergency.html',{'uid':uid,'contacts':contacts,"msg":"Contact has been added"})

    return render(request,'emergency.html',{'uid':uid,'contacts':contacts})


def del_emergency(request,pk):
    d = Emergency.objects.get(id=pk)
    d.delete()
    return redirect('emergency')

def add_member(request):
    uid = SecUser.objects.get(email=request.session['email'])
    members = mm.Member.objects.all().order_by('flat_no')
    if request.method == 'POST':
        try:
            mm.Member.objects.get(email=request.POST['email'])
            msg = 'Email is Already register'
            return render(request,'add-member.html',{'uid':uid,'members':members,'msg':msg})

        except:
            s = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890@.1234567890'
            password = ''.join(choices(s,k=8))
            subject = 'Welcome to Society Management App'
            message = f"""Hello {request.POST["email"]}, 
            Your Account is created for Society Network. 
            Your login credentials are 

            Username : {request.POST['email']}
            Password : {password}
            Keep it secret and please change password after login."""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )

            mm.Member.objects.create(
                fname = request.POST['fname'],
                lname = request.POST['lname'],
                email = request.POST['email'],
                mobile = request.POST['mobile'],
                doc = request.POST['doc'],
                doc_number = request.POST['dnumber'],
                flat_no = request.POST['flat_no'],
                address = request.POST['address'],
                password = password,
                verify = True if 'verify' in request.POST else False
            )
            return render(request,'add-member.html',{'uid':uid,'members':members,'msg':'User Created'})
    return render(request,'add-member.html',{'uid':uid,'members':members})

def del_member(request,pk):
    member = mm.Member.objects.get(id=pk)
    member.delete()
    return redirect('add-member')
