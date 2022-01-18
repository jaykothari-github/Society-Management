from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name='member-index'),
    path('member-login/',views.member_login,name='member-login'),
    path('member-logout/',views.logout,name='member-logout'),
    path('member-profile/',views.profile,name='member-profile'),
    path('member-change-password/',views.change_password,name='member-change-password'),
    path('emergency-contact/',views.emergency_contact,name='emergency-contact'),
<<<<<<< HEAD
    path('member-view-notices/',views.view_notice,name='member-view-notices'),
    path('member-view-notice/<int:pk>',views.view_my_notice,name='member-view-notice'),
    path('member-gallery/',views.member_gallery,name='member-gallery'),
=======
    path('member-view-notice/',views.view_notice,name='member-view-notice'),
    path('view-single-notice/<int:pk>',views.view_single_notice,name='view-single-notice'),
>>>>>>> 631f985a7af7a6d02aa8d30245febf1a839a171c
]