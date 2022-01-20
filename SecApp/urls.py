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
    path('emergency/',views.emergency,name='emergency'),
    path('delete-emergency/<int:pk>',views.del_emergency,name='delete-emergency'),
    path('delete-member/<int:pk>',views.del_member,name='delete-member'),
    path('edit-member/<int:pk>',views.edit_member, name='edit-member'),
    path('add-member/',views.add_member, name='add-member'),
    path('add-event/',views.add_event, name='add-event'),
    path('edit-event/<int:pk>',views.edit_event, name='edit-event'),
    path('delete-event/<int:pk>',views.delete_event, name='delete-event'),
    path('send-notice/',views.send_notice, name='send-notice'),
    path('view-send-notice/<int:pk>',views.view_send_notice, name='view-send-notice'),
    path('gallery/',views.gallery, name='gallery'),
    path('manage-complans/',views.manage_complains, name='manage-complains'),
    path('complain-status/<int:pk>',views.complain_status,name='complain-status'),
    path('view-complain/<int:pk>',views.view_complain,name='view-complain'),

]
