from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Profile, Message, CommunityChat, Bubblemate_chat, CommunityResponse

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))

class SignupForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')
    
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
        'class': 'w-full py-4 px-6 rounded-xl'
    }))


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['description', 'interests', 'profile_pic']
        widgets = {
            'description': forms.TextInput(attrs={'class': 'w-full py-4 px-6 rounded-xl', 'placeholder': 'Description'}),
            'interests': forms.SelectMultiple(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
            'profile_pic': forms.FileInput(attrs={'class': 'w-full py-4 px-6 rounded-xl'}),
        }

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['chat'] 

class CommunityChatForm(forms.ModelForm):
    class Meta:
        model = CommunityChat
        fields = ['title', 'message']

class BubbleMateChatForm(forms.ModelForm):
    class Meta:
        model = Bubblemate_chat
        fields = ['chat']

class BubblePostResponseForm(forms.ModelForm):
    class Meta:
        model = CommunityResponse
        fields = ['message']