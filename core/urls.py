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
    path('mybubbles/', views.mybubbles, name='mybubbles'),
    path('myfriends/', views.myfriends, name='myfriends'),
    path('bubble/<int:pk>/', views.bubble, name='bubble'),
    path('friend_profile/<str:friend_username>/', views.friend_profile_view, name='friend_profile_view'),
    path('friend_chat/<str:friend_username>/', views.friend_chat, name='friend_chat'),
    path('bubble/<int:pk>/mate_chat/<str:username>/', views.bubble_mate_chat, name='bubble_mate_chat'),
    path('bubble/<int:pk>/bubble_post/<int:post_id>/', views.bubble_post, name='bubble_post'),



    #path('', views.dashboard, name='dashboard'),
]