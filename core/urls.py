from django.contrib.auth import views as auth_views
from django.urls import path
from . import views
from .forms import LoginForm

app_name = 'core'

urlpatterns = [
    path('', views.home, name= 'index'),
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='core/login.html', authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', views.user_profile, name='user_profile'),
    path('update-profile/', views.update_profile, name='update_profile'),

    #bubble entry questions
    path('entrytest/<int:test_id>/', views.test_view, name='test_view'),
    path('update_option_response/', views.update_option_response, name='update_option_response'), #json responce to questions
    path('answer_question/', views.answer_question, name='answer_question'),
    path('submit-entry-test/<int:entry_test_id>/', views.submit_entry_test, name='submit_entry_test'),

    #core pages
    path('mybubbles/', views.mybubbles, name='mybubbles'),
    path('myfriends/', views.myfriends, name='myfriends'),

    #Bubbles
    path('bubble/<int:pk>/', views.bubble, name='bubble'),
    path('fetch-post/<int:pk>/', views.fetch_post, name='fetch_post'),
    path('post-post/<int:pk>/', views.post_post, name='post_post'),
    path('swipe/<int:target_user_id>/<str:action>/', views.swipe_view, name='swipe'),
    path('bubble/<int:pk>/bubble_post/<int:post_id>/', views.bubble_post, name='bubble_post'),
    path('bubble/<int:pk>/bubble_post_fetch_response/<int:post_id>/', views.fetch_post_response, name='fetch_post_response'),
    path('bubble/<int:pk>/bubble_post_post_response/<int:post_id>/', views.post_post_response, name='post_post_response'),
    
    #Friends Chat
    path('friend_profile/<str:friend_username>/', views.friend_profile_view, name='friend_profile_view'),
    path('friend_chat/<str:friend_username>/', views.friend_chat, name='friend_chat'),
    path('friend_chat_all/<str:friend_username>/', views.friend_chat_all, name='friend_chat_all'),
    path('fetch-comments/<str:friend_username>/', views.fetch_comments, name='fetch_comments'),
    path('post-message/<str:friend_username>/', views.post_message, name='post_message'),

    #Bubble mate
    path('bubble/<int:pk>/mate_chat/<str:username>/', views.bubble_mate_chat, name='bubble_mate_chat'),
    path('fetch_chat_bubble_mate/<int:pk>/<str:username>/', views.fetch_chat_bubble_mate, name='fetch_chat_bubble_mate'),
    path('post_chat_bubble_mate/<int:pk>/<str:username>/', views.post_chat_bubble_mate, name='post_chat_bubble_mate'),
    

    #Notifiation
    path('get-message-count/<int:sender_id>/', views.get_message_count, name='get-message-count'),
    path('reset-message-count/<int:sender_id>/', views.reset_message_count, name='reset-message-count'),

    path('get-bubble-message-count/<int:sender_id>/<int:pk>/', views.get_bubble_message_count, name='get-bubble-message-count'),
    path('reset-bubble-message-count/<int:sender_id>/<int:pk>/', views.reset_bubble_message_count, name='reset-bubble-message-count'),



    #path('', views.dashboard, name='dashboard'),
]