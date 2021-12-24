from django.urls import path
from . import views

urlpatterns = [
    path('',views.signin,name='sign-in'),
    path('sign-up/',views.signup,name='sign-up'),
    path('otp/',views.OTP,name='otp'),
    path('logout/',views.logout,name='logout'),
    path('forgot-password/',views.forgot_password,name='forgot-password'),
    path('index/',views.index,name='index'),
    path('profile/',views.profile,name='profile'),
    path('change-password/',views.change_password,name='change-password'),
]
