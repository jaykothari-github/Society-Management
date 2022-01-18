from django.shortcuts import redirect, render
from .models import *
from SecApp import models as sm

# Create your views here.

def index(request):
    event_count = Event.objects.all().count()
    member_count = Member.objects.all().count()
    try:
        member = Member.objects.get(email=request.session['memail'])
        photos = list(sm.Gallery.objects.all())[-8:]
        return render(request,'member-index.html',{'member':member,'photos':photos,'event_count':event_count,'member_count':member_count})
    except:
        return render(request,'member-index.html',{'event_count':event_count,'member_count':member_count})

def member_login(request):
    try:
        Member.objects.get(email=request.session['memail'])
        return redirect('member-index')
    except:
        if request.method == 'POST':
            try:
                uid = Member.objects.get(email=request.POST['email'])
                if request.POST['password'] == uid.password:
                    request.session['memail'] = request.POST['email']
                    return redirect('member-index')
            except:
                msg = "You Don't have an Account request to secratory for an account."
                return render(request,'member-login.html',{'msg':msg})
            
        return render(request,'member-login.html')

def logout(request):
    del request.session['memail']
    return redirect('member-index')

def profile(request):
    mem = Member.objects.get(email=request.session['memail'])
    if request.method == 'POST':
        mem.fname = request.POST['fname']
        mem.lname = request.POST['lname']
        mem.mobile = request.POST['mobile']
        mem.address = request.POST['address']
        if 'pic' in request.FILES:
            mem.pic = request.FILES['pic']
        mem.save()
        msg = 'Profile has been updated'
        return render(request,'member-profile.html',{'member':mem,'msg':msg})
    return render(request,'member-profile.html',{'member':mem})

def change_password(request):
    mem = Member.objects.get(email=request.session['memail'])
    if request.method == 'POST':
        if mem.password == request.POST['old_password']:
            if request.POST['new_password'] == request.POST['con_password']:
                mem.password = request.POST['new_password']
                mem.save()
                return render(request,'member-change-password.html',{'member':mem,'msg':'Password Has been updated'})
            return render(request,'member-change-password.html',{'member':mem,'msg':'New passwords are not same'})
        return render(request,'member-change-password.html',{'member':mem,'msg':'Old Password is not matched'})
    return render(request,'member-change-password.html',{'member':mem})

def emergency_contact(request):
    contacts = sm.Emergency.objects.all()
    member = Member.objects.get(email=request.session['memail'])
    if request.method == 'POST':
        if request.POST['cate'] == 'all':
            contacts = sm.Emergency.objects.all()
        else:
            contacts = sm.Emergency.objects.filter(occupation=request.POST['cate'])
    
    return render(request,'emergency-contact.html',{'member':member,'contacts':contacts})

def view_notice(request):
    member = Member.objects.get(email=request.session['memail'])
    notices = Notice.objects.filter(member=member)[::-1]
    return render(request,'view-notice.html',{'notices':notices,'member':member})