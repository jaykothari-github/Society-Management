from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='member-index'),
    path('member-login/',views.member_login,name='member-login'),
    path('member-logout/',views.logout,name='member-logout'),
    path('member-profile/',views.profile,name='member-profile'),
    path('member-change-password/',views.change_password,name='member-change-password'),
]