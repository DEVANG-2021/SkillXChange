from django.contrib import admin
from django.urls import path
from .views.home import Index 
from .views.signup import Signup,update_image, update_personal_details, update_social_links, update_license_details
from .views.login import Login , logout
from .views.profile import Profile1
from .middlewares.auth import  auth_middleware
from .views.search import search_customers
from .views.chat_message import customer_list,chat_window,showHtml
from .views.credit import send_credit
from .views.send_email import send_invitation_email
from .views.schedule_meeting import schedule_meeting,schedule_meeting_page,scheduled_meetings
from .views.room import lobby,room,getToken,createMember,getMember,deleteMember
from .views.cookies import track_daily_visits
from .views.forgotpassword import forgot_password,reset_password
from .views.ratings import rate_customer
from .views.video_call import videocall,join_room


urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('home', Index.as_view() , name='home'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    # profile
    path('profile', Profile1.as_view(), name='profile'),
    # path('users/<int:customer_id>/', Profile1.user, name='user'),
    path('logout', logout , name='logout'),
    path('search/', search_customers, name='search_customers'),

    path('requests/', Profile1.requests_page, name='requests_page'),
    path('user/<int:user_id>/', Profile1.user_profile, name='user_profile'),
    path('send-request/<int:receiver_id>/', Profile1.send_request, name='send_request'),
    path('withdraw_request/<int:request_id>/', Profile1.withdraw_request, name='withdraw_request'),
    path('accept_request/<int:request_id>/', Profile1.accept_request, name='accept_request'),
    path('reject_request/<int:request_id>/', Profile1.reject_request, name='reject_request'),
    path('notifications/', Profile1.notifications_page, name='notifications_page'),

    path('customers/', customer_list, name='customer_list'),
    path('chat/<int:customer_id>/', chat_window, name='chat_window'),

    path('send_credit', send_credit, name='send_credit'),
    path('send_email', send_invitation_email, name='send_email'),
    
    # video Integration
    path('schedule_meeting/', schedule_meeting, name='schedule_meeting'),
    path('schedule_meeting_page/', schedule_meeting_page, name='schedule_meeting_page'),

    path('lobby/', lobby, name='lobby'),
    path('room/', room, name='room'),
    path('get_token/', getToken, name='get_token'),
    path('scheduled_meetings/', scheduled_meetings, name='scheduled_meetings'),
    
    path('create_member/', createMember,name='create_member'),
    path('get_member/', getMember,name='get_member'),
    path('delete_member/', deleteMember,name='delete_member'),

    # Cookie : track daily visit of user for analytics purpose
    path('track_daily_visits/', track_daily_visits,name='track_daily_visits'),

    # Forgot Password functionality 
    path('forgot-password/', forgot_password, name='forgot_password'),
    path('reset-password/<str:uidb64>/', reset_password, name='reset_password'),
    
    path('rate_customer', rate_customer, name='rate_customer'),

    path('update/image/', update_image, name='update_image'),
    path('update/personal-details/', update_personal_details, name='update_personal_details'),
    path('update/social-links/', update_social_links, name='update_social_links'),
    path('update/license-details/', update_license_details, name='update_license_details'),
    # path('chat_page', showHtml, name='chat_page'),
    # path('chat_page1', Profile1.index, name='chat_page1'),
    # path("<str:room_name>/", Profile1.room, name="room"),

    # new routes for meeting
    path('meeting/',videocall, name='meeting'),
    path('join/',join_room, name='join_room'),
]