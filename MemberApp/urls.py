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
    path('member-gallery/',views.member_gallery,name='member-gallery'),
    path('member-complain/',views.member_complain,name='member-complain'),
    path('member-view-complain/',views.member_view_complain,name='member-view-complain'),
    path('member-detail-complain/<int:pk>',views.member_detail_complain,name='member-detail-complain'),
]