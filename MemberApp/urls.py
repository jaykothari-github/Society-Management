from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='member-index'),
    path('member-login/',views.member_login,name='member-login'),
    path('member-logout/',views.logout,name='member-logout'),
    path('member-profile/',views.profile,name='member-profile'),
    path('member-change-password/',views.change_password,name='member-change-password'),
    path('emergency-contact/',views.emergency_contact,name='emergency-contact'),
    path('member-view-notices/',views.view_notice,name='member-view-notices'),
    path('member-view-notice/<int:pk>',views.view_my_notice,name='member-view-notice'),
]