from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from core.models import BubbleMember, Bubble, Profile, CommunityChat, Bubblemate_chat, CommunityResponse
from django.contrib.auth.models import User
from .forms import ProfileUpdateForm, MessageForm, CommunityChatForm, BubbleMateChatForm, BubblePostResponseForm


def home(request):
    return render(request, 'core/home.html',)

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)

        if form.is_valid():
            form.save()

            return redirect('/login/')
    else:
        form = SignupForm()

    return render(request, 'core/signup.html', {
        'form': form
    })


from core.models import Profile

@login_required
def user_profile(request):
    username = request.user.username
    user_id = request.user.id

    try:
        profile = Profile.objects.get(user_id=user_id)
    except Profile.DoesNotExist:
        # If Profile does not exist, create a new Profile instance
        profile = Profile.objects.create(user_id=request.user)

    return render(request, 'core/user_profile.html', {
        'username': username,
        'profile': profile
    })

@login_required
def update_profile(request):
    user_id = request.user.id
    profile = Profile.objects.get(user_id=user_id)
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('core:user_profile')  # Redirect to a success page or profile view
    else:
        form = ProfileUpdateForm(instance=profile)

    return render(request, 'core/update_profile.html', {'form': form})


from core.decorators import  friend_required


@friend_required
def friend_profile_view(request, friend_username):
    friend_profile = get_object_or_404(User, username=friend_username)
    logged_in_user_profile = request.user  # Assuming profile is linked to User

    return render(request, 'core/friend_profile.html', {
        'friend_profile': friend_profile,
        'logged_in_user_profile': logged_in_user_profile,
    })


@friend_required
def friend_chat(request, friend_username):
    friend_profile = get_object_or_404(User, username=friend_username)
    friend_username = friend_username
    logged_in_user_profile = request.user  # Assuming profile is linked to User





    return render(request, 'core/friend_chat.html', {
        'friend_profile': friend_profile,
        'friend_username' : friend_username,
        'logged_in_user_profile': logged_in_user_profile,
        
        
    })

from django.http import JsonResponse
from django.db.models import Q
from .models import Message
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User

def fetch_comments(request, friend_username):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        friend_profile = get_object_or_404(User, username=friend_username)
        logged_in_user_profile = request.user

        # Count the total number of chats
        total_chats = Message.objects.filter(
            Q(sender=friend_profile, receiver=logged_in_user_profile) |
            Q(sender=logged_in_user_profile, receiver=friend_profile)
        ).count()

        # Fetch the latest 10 chats only if there are more than 10 chats
        if total_chats > 10:
            chats = Message.objects.filter(
                Q(sender=friend_profile, receiver=logged_in_user_profile) |
                Q(sender=logged_in_user_profile, receiver=friend_profile)
            ).order_by('-created_at')[:10]
            # Reorder the fetched messages by 'created_at' in ascending order
            chats = sorted(chats, key=lambda x: x.created_at)
        else:
            chats = Message.objects.filter(
                Q(sender=friend_profile, receiver=logged_in_user_profile) |
                Q(sender=logged_in_user_profile, receiver=friend_profile)
            ).order_by('created_at')

        chat_data = [{
            "sender": chat.sender.username,
            "message": chat.chat,
            "created_at": chat.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for chat in chats]

        return JsonResponse({"chats": chat_data})
    else:
        # Handle non-AJAX requests here
        pass



def post_message(request, friend_username):
    friend_profile = get_object_or_404(User, username=friend_username)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = friend_profile
            message.save()
            return JsonResponse({'status': 'success', 'message': message.chat })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})




@login_required
def mybubbles(request):
    user = request.user
    user_bubbles = BubbleMember.objects.filter(user_id=user.id)
    return render(request, 'core/MyBubbles.html', {'user_bubbles': user_bubbles})


from core.models import Message, Friend
from django.db.models import Q

@login_required
def myfriends(request):
    user = request.user
    user_friends_id = (
        Friend.objects.filter(Q(user1=user.id) | Q(user2=user.id))
        .values_list('user1_id', flat=True)
        .union(Friend.objects.filter(Q(user1=user.id) | Q(user2=user.id)).values_list('user2_id', flat=True))
    )

    user_friends = []
    
    for friends in user_friends_id:
        user = User.objects.get(pk=friends)
        user_friends.append(user)

    return render(request, 'core/MyFriends.html', {'user_friends': user_friends})

from core.decorators import part_of_bubble_required, friend_required

@part_of_bubble_required
def bubble(request, pk):
    bubble = get_object_or_404(Bubble, pk=pk)
    Bubble_id = bubble.id
    members_in_bubble = BubbleMember.objects.filter(bubble_id=Bubble_id) 

    #List of community Chats

    Community_Posts = CommunityChat.objects.filter(bubble_id = Bubble_id).order_by('created_on')


    #new Comunity Chats
    if request.method == 'POST':
        form = CommunityChatForm(request.POST)
        if form.is_valid():
            community_chat = form.save(commit=False)
            community_chat.bubble_id = bubble
            community_chat.user = BubbleMember.objects.get(bubble_id=Bubble_id, user_id=request.user )  # Assuming user is authenticated
            community_chat.save()
            form = CommunityChatForm()  # Clear the form after successful submission
    else:
        form = CommunityChatForm()

    return render(request, 'core/bubble.html' , {
        'bubble' : bubble,
        'members_in_bubble' : members_in_bubble,
        'form': form,
        'Community_Posts': Community_Posts,
    })

@part_of_bubble_required
def bubble_post(request, pk, post_id):
    bubble = get_object_or_404(Bubble, pk=pk)
    logged_in_user_profile = request.user
    bubble_post = get_object_or_404(CommunityChat, id=post_id)

    #list of reponses to bubble post
    responses = CommunityResponse.objects.filter(original_chat=bubble_post).order_by('created_on')

    #response form
    if request.method == 'POST':
        form = BubblePostResponseForm(request.POST)
        if form.is_valid():
            community_response = form.save(commit=False)
            community_response.original_chat = bubble_post
            # Assuming BubbleMember is associated with the logged-in user
            bubble_member = get_object_or_404(BubbleMember, bubble_id=bubble, user_id=request.user)
            community_response.user = bubble_member
            community_response.save()
            form = BubblePostResponseForm()  # Clear the form after successful submission
    else:
        form = BubblePostResponseForm()

    return render(request, 'core/bubble_post.html', {
        'bubble_post' : bubble_post,
        'form': form,
        'responses': responses,
    })



@part_of_bubble_required
def bubble_mate_chat(request, pk, username):
    bubble = get_object_or_404(Bubble, pk=pk)
    friend_profile = get_object_or_404(User, username=username)
    logged_in_user_profile = request.user
    bubble_friend_profile = BubbleMember.objects.get(bubble_id=bubble, user_id=friend_profile )
    Bubble_logged_in_user_profile = BubbleMember.objects.get(bubble_id=bubble, user_id=logged_in_user_profile )

    chat = Bubblemate_chat.objects.filter(
        Q(sender=bubble_friend_profile, receiver=Bubble_logged_in_user_profile, bubble_id=bubble) | 
        Q(sender=Bubble_logged_in_user_profile, receiver=bubble_friend_profile,bubble_id=bubble)
        ).order_by('created_at')


    #bubble mate form
    if request.method == 'POST':
        form = BubbleMateChatForm(request.POST)
        if form.is_valid():
            bubble_mate_chat = form.save(commit=False)
            bubble_mate_chat.bubble_id = bubble
            bubble_mate_chat.sender = BubbleMember.objects.get(bubble_id=bubble, user_id=request.user )
            bubble_mate_chat.receiver = BubbleMember.objects.get(bubble_id=bubble, user_id=friend_profile )
            bubble_mate_chat.save()
            form = BubbleMateChatForm()  # Clear the form after successful submission
    else:
        form = BubbleMateChatForm()

    return render(request, 'core/bubble_mate_chat.html', {
        'chat': chat,
        'friend_profile': friend_profile,
        'form': form,
    })