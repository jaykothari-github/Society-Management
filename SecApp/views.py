import re
from django.db.models.manager import EmptyManager
from django.http.response import Http404, HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from .models import *
from django.conf import settings
from django.core.mail import send_mail
from random import randrange, choices
from MemberApp import models as mm
from datetime import datetime


# Create your views here.

def signin(request):
    try: 
        SecUser.objects.get(email=request.session['email'])
        return redirect('index')
    except:
        if request.method == 'POST':
            try:
                uid = SecUser.objects.get(email=request.POST['email'])
                if uid.password == request.POST['password']:
                    request.session['email'] = request.POST['email']
                    return redirect('index')
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
        mem_count = mm.Member.objects.all().count()
        event_count = mm.Event.objects.all().count()
        complain_count = mm.Complain.objects.filter(status=False).count()
        try:
            new_members = mm.Member.objects.all()[-5:]
            complains = mm.Complain.objects.filter(status=False)[-1:-7:-1]
        except:
            complains = mm.Complain.objects.filter(status=False)
            new_members = mm.Member.objects.all()[::-1]

        return render(request,'index.html',{'uid':uid,'complain_count':complain_count,'complains':complains,'new_members':new_members,'mem_count':mem_count,'event_count':event_count})

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
        contacts = Emergency.objects.all()[::-1]
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
            message = f"""Hello {request.POST["fname"]} {request.POST['lname']}, 
            Your Account is created for Society Network. 
            Your login credentials are 

            Username : {request.POST['email']}
            Password : {password}
            Keep it secret and please change password after login."""
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [request.POST['email'], ]
            send_mail( subject, message, email_from, recipient_list )

            mm.Member.objects.create(
                uid = uid,
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
    # list_m = mm.Member.objects.values_list('email',flat=True)
    # print(list(list_m))
    return render(request,'add-member.html',{'uid':uid,'members':members})

def del_member(request,pk):
    member = mm.Member.objects.get(id=pk)
    member.delete()
    return redirect('add-member')

def edit_member(request,pk):
    uid = SecUser.objects.get(email=request.session['email'])
    member = mm.Member.objects.get(id=pk)
    if request.method == 'POST':
        member.uid = uid
        member.fname = request.POST['fname']
        member.lname = request.POST['lname']
        member.email = request.POST['email']
        member.mobile = request.POST['mobile']
        member.doc = request.POST['doc']
        member.doc_number = request.POST['dnumber']
        member.flat_no = request.POST['flat_no']
        member.address = request.POST['address']
        member.verify = True if 'verify' in request.POST else False
        member.role = request.POST['role']
        member.save()
        return redirect('add-member')
    return render(request,'edit-member.html',{'uid':uid,'member':member})

def add_event(request):
    uid = SecUser.objects.get(email=request.session['email'])
    events = mm.Event.objects.all()[::-1]

    if request.method == 'POST':
        mm.Event.objects.create(
            uid = uid,
            event_name = request.POST['ename'],
            event_des = request.POST['edes'],
            event_at = request.POST['edate'],
            pic = request.FILES['pic'] if 'pic' in request.FILES else None
        )
        events = mm.Event.objects.all()[::-1]
        subject = 'New Event Added into Society'
        message = f"""Hello User!!, 
        New Event has schedule in your society. Have you gone through it?? 
        Event Details are : 
        Event name : {request.POST['ename']}
        Event date : {request.POST['edate']}

        Event Description : {request.POST['edes']}
        ---------------------------------------------
        and Posted by : {uid.name} / secratory of Society."""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = list(mm.Member.objects.values_list('email',flat=True))
        send_mail( subject, message, email_from, recipient_list )
        return render(request,'add-event.html',{'uid':uid,'events':events,'msg':'Event Added Successfully'})
    return render(request,'add-event.html',{'uid':uid,'events':events})

def edit_event(request,pk):
    uid = SecUser.objects.get(email=request.session['email'])
    event = mm.Event.objects.get(id=pk)
    event_at = str(event.event_at)
    if request.method == 'POST':
        event.uid = uid
        event.event_name = request.POST['ename']
        event.event_des = request.POST['edes']
        event.event_at = request.POST['edate']
        event.pic = None if 'pic' not in request.FILES else request.FILES['pic'] 
        event.save()
        events = mm.Event.objects.all()[::-1]
        return render(request,'add-event.html',{'uid':uid,'msg':'Event Updated','events':events})
    return render(request,'edit-event.html',{'uid':uid,'event':event,'event_at':event_at})

def delete_event(request,pk):
    event = mm.Event.objects.get(id=pk)
    event.delete()
    return redirect('add-event')

def send_notice(request):
    uid = SecUser.objects.get(email=request.session['email'])
    members = mm.Member.objects.all()
    notices = mm.Notice.objects.all()[::-1]
    if request.method == 'POST':
        member = mm.Member.objects.get(id=request.POST['member'])
        mm.Notice.objects.create(
            uid = uid,
            member = member,
            subject = request.POST['subject'],
            des = request.POST['des'],
            pic = request.FILES['pic'] if 'pic' in request.FILES else None
        )
        subject = 'You got a notice from Secratory'
        message = f"""Hello {member.fname} {member.lname}!!, 
        
        You got a notice from secratory for : {request.POST['subject']}
        from : {uid.name}, Secratory of the society
        for further details visit your member account."""
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [member.email,]
        send_mail( subject, message, email_from, recipient_list )
        notices = mm.Notice.objects.all()[::-1]
        
        return render(request,'send-notice.html',{'members':members,'uid':uid,'notices':notices,'msg':'Notice sent to member'})
    return render(request,'send-notice.html',{'members':members,'notices':notices,'uid':uid})

def view_send_notice(request,pk):
    uid = SecUser.objects.get(email=request.session['email'])
    notice = mm.Notice.objects.get(id=pk)
    return render(request,'view-send-notice.html',{'uid':uid,'notice':notice})

def gallery(request):
    uid = SecUser.objects.get(email=request.session['email'])
    if request.FILES:
        Gallery.objects.create(
            uid = uid,
            pic = request.FILES['pic']
        )
    photos = Gallery.objects.all()[::-1]
    return render(request,'gallery.html',{'photos':photos,'uid':uid})

def manage_complains(request):
    uid = SecUser.objects.get(email=request.session['email'])
    complains = mm.Complain.objects.all()[::-1]
    return render(request,'manage-complains.html',{'complains':complains,'uid':uid})

def complain_status(request,pk):
    complain = mm.Complain.objects.get(id=pk)
    uid = SecUser.objects.get(email=request.session['email'])
    complain.solve_by = uid
    complain.status = True
    complain.solved_at = datetime.now()
    complain.save()
    return redirect('manage-complains')
    
def view_complain(request,pk):
    uid = SecUser.objects.get(email=request.session['email'])
    complain = mm.Complain.objects.get(id=pk)
    return render(request,'view-complain.html',{'uid':uid,'complain':complain})