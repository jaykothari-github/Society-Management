from django.shortcuts import redirect, render
from .models import *


# Create your views here.

def index(request):
    event_count = Event.objects.all().count()
    member_count = Member.objects.all().count()
    try:
        member = Member.objects.get(email=request.session['memail'])
        return render(request,'member-index.html',{'member':member,'event_count':event_count,'member_count':member_count})
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
    mem = Member.objects.get(email=request.session['email'])
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

def  change_password(request):
    return render(request,'member-change-password.html')