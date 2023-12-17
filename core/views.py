from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.contrib.auth.decorators import login_required
from core.models import BubbleMember, Bubble, Profile, CommunityChat, Bubblemate_chat, CommunityResponse, EntryTestSubmit
from django.contrib.auth.models import User
from .forms import ProfileUpdateForm, MessageForm, CommunityChatForm, BubbleMateChatForm, BubblePostResponseForm


def home(request):
    entry_forum = EntryTest.objects.filter(state='active').first()
    # Check if entry_forum exists and user is authenticated
    test_submit = False
    if entry_forum and request.user.is_authenticated:
        # Get or create the EntryTestSubmit object
        test_submit, created = EntryTestSubmit.objects.get_or_create(
            entryTest=entry_forum, 
            user=request.user,
            defaults={'Submit': False}  # You can set the default value for Submit here
        )
    user_bubbles = BubbleMember.objects.filter(user_id=request.user.id)
    active_bubbles = []
    for bubble in user_bubbles:
        bub = bubble.bubble_id
        if bub.status=='1':
            active_bubbles.append(bub)
    return render(request, 'core/home.html',{
        'entry_forum': entry_forum,
        'test_submit': test_submit,
        'active_bubbles': active_bubbles,
    })

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

@friend_required
def friend_chat_all(request, friend_username):
    friend_profile = get_object_or_404(User, username=friend_username)
    friend_username = friend_username
    logged_in_user_profile = request.user  # Assuming profile is linked to User
    chats = Message.objects.filter(
                Q(sender=friend_profile, receiver=logged_in_user_profile) |
                Q(sender=logged_in_user_profile, receiver=friend_profile)
            ).order_by('-created_at')

    return render(request, 'core/friend_chat_all.html', {
        'friend_profile': friend_profile,
        'friend_username' : friend_username,
        'logged_in_user_profile': logged_in_user_profile,
        'chats' : chats
        
        
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

        response = JsonResponse({"chats": chat_data})
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'

        return response
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

            # Update or create the MessageNotification
            notification, created = MessageNotification.objects.get_or_create(
                receiver=friend_profile, sender=request.user, 
                defaults={'unread_count': 1}
            )
            if not created:
                notification.unread_count += 1
                notification.save()

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
        Friend.objects.filter((Q(user1=user.id)  | Q(user2=user.id) ) & Q(status1='accepted') & Q(status2='accepted'))
        .values_list('user1_id', flat=True)
        .union(Friend.objects.filter((Q(user1=user.id)  | Q(user2=user.id) ) & Q(status1='accepted') & Q(status2='accepted')).values_list('user2_id', flat=True))
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

    #my friend list
    user = request.user
    user_friends_id = (
        Friend.objects.filter((Q(user1=user.id)  | Q(user2=user.id) ) & Q(status1='accepted') & Q(status2='accepted'))
        .values_list('user1_id', flat=True)
        .union(Friend.objects.filter((Q(user1=user.id)  | Q(user2=user.id) ) & Q(status1='accepted') & Q(status2='accepted')).values_list('user2_id', flat=True))
    )

    user_friends = []
    
    for friends in user_friends_id:
        user = User.objects.get(pk=friends)
        user_friends.append(user)

    #my friend list pending
    user_friends_id_pending = (
        Friend.objects.filter((Q(user1=user.id)  | Q(user2=user.id) ))
        .values_list('user1_id', flat=True)
        .union(Friend.objects.filter((Q(user1=user.id)  | Q(user2=user.id) )).values_list('user2_id', flat=True))
    )

    user_friends_pending = []

    for friend_id in user_friends_id_pending:
        try:
            # Check if the current user is user1 in the friendship
            friendship = Friend.objects.get(user1=user.id, user2=friend_id)
            if friendship.status1 == Friend.ACCEPTED:
                friend_user = User.objects.get(pk=friend_id)
                user_friends_pending.append(friend_user)
        except Friend.DoesNotExist:
            pass  # Friend object not found for this combination

        try:
            # Check if the current user is user2 in the friendship
            friendship = Friend.objects.get(user2=user.id, user1=friend_id)
            if friendship.status2 == Friend.ACCEPTED:
                friend_user = User.objects.get(pk=friend_id)
                user_friends_pending.append(friend_user)
        except Friend.DoesNotExist:
            pass  # Friend object not found for this combination
      
    
    return render(request, 'core/bubble.html' , {
        'bubble' : bubble,
        'members_in_bubble' : members_in_bubble,
        'user_friends': user_friends,
        'user_friends_pending':user_friends_pending,
    })

def fetch_post(request, pk):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        bubble = get_object_or_404(Bubble, pk=pk)
        Bubble_id = bubble.id

        #List of community Chats
        Community_Posts = CommunityChat.objects.filter(bubble_id = Bubble_id).order_by('created_on')

        post_data = [{
            "sender": Community_Post.user.user_id.username,
            "title": Community_Post.title,
            "message": Community_Post.message,
            "created_at": Community_Post.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "post_id": Community_Post.id
        } for Community_Post in Community_Posts]

        response = JsonResponse({"posts": post_data})
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    else:
        # Handle non-AJAX requests here
        pass
    

def post_post(request, pk):
    bubble = get_object_or_404(Bubble, pk=pk)
    Bubble_id = bubble.id
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = CommunityChatForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.bubble_id = bubble
            post.user = BubbleMember.objects.get(bubble_id=Bubble_id, user_id=request.user )
            post.save()
            return JsonResponse({'status': 'success', 'message': post.message })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@part_of_bubble_required
def bubble_mate_chat(request, pk, username):
    bubble = get_object_or_404(Bubble, pk=pk)
    friend_profile = get_object_or_404(User, username=username)
    logged_in_user_profile = request.user
    bubble_friend_profile = BubbleMember.objects.get(bubble_id=bubble, user_id=friend_profile )
    Bubble_logged_in_user_profile = BubbleMember.objects.get(bubble_id=bubble, user_id=logged_in_user_profile )

    return render(request, 'core/bubble_mate_chat.html', {
        'friend_profile': friend_profile,
        'pk': pk,
        'username':username,
        'bubble':bubble,
    })

def fetch_chat_bubble_mate(request, pk, username):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        bubble = get_object_or_404(Bubble, pk=pk)
        friend_profile = get_object_or_404(User, username=username)
        logged_in_user_profile = request.user
        bubble_friend_profile = BubbleMember.objects.get(bubble_id=bubble, user_id=friend_profile )
        Bubble_logged_in_user_profile = BubbleMember.objects.get(bubble_id=bubble, user_id=logged_in_user_profile )

        # Count the total number of chats
        total_chats = Bubblemate_chat.objects.filter(
        Q(sender=bubble_friend_profile, receiver=Bubble_logged_in_user_profile, bubble_id=bubble) | 
        Q(sender=Bubble_logged_in_user_profile, receiver=bubble_friend_profile,bubble_id=bubble)
        ).count()

        # Fetch the latest 10 chats only if there are more than 10 chats
        if total_chats > 10:
            chats = Bubblemate_chat.objects.filter(
                Q(sender=bubble_friend_profile, receiver=Bubble_logged_in_user_profile, bubble_id=bubble) | 
                Q(sender=Bubble_logged_in_user_profile, receiver=bubble_friend_profile,bubble_id=bubble)
            ).order_by('-created_at')[:10]
            # Reorder the fetched messages by 'created_at' in ascending order
            chats = sorted(chats, key=lambda x: x.created_at)
        else:
            chats = Bubblemate_chat.objects.filter(
                Q(sender=bubble_friend_profile, receiver=Bubble_logged_in_user_profile, bubble_id=bubble) | 
                Q(sender=Bubble_logged_in_user_profile, receiver=bubble_friend_profile,bubble_id=bubble)
            ).order_by('created_at')

        chat_data = [{
            "sender": chat.sender.user_id.username,
            "message": chat.chat,
            "created_at": chat.created_at.strftime("%Y-%m-%d %H:%M:%S")
        } for chat in chats]

        response = JsonResponse({"chats": chat_data})
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    else:
        # Handle non-AJAX requests here
        pass

def post_chat_bubble_mate(request, pk, username):
    bubble = get_object_or_404(Bubble, pk=pk)
    friend_profile = get_object_or_404(User, username=username)
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = BubbleMateChatForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.bubble_id = bubble
            message.sender = BubbleMember.objects.get(bubble_id=bubble, user_id=request.user )
            message.receiver = BubbleMember.objects.get(bubble_id=bubble, user_id=friend_profile )
            message.save()
            # Update or create the MessageNotification

            return JsonResponse({'status': 'success', 'message': message.chat })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


@part_of_bubble_required
def bubble_post(request, pk, post_id):
    bubble = get_object_or_404(Bubble, pk=pk)
    logged_in_user_profile = request.user
    bubble_post = get_object_or_404(CommunityChat, id=post_id)

    requestuser_secretname = request.user.id
    
    return render(request, 'core/bubble_post.html', {
        'requestuser_secretname': requestuser_secretname,
        'bubble': bubble,
        'bubble_post' : bubble_post,
    })


def fetch_post_response(request, pk, post_id):
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        bubble = get_object_or_404(Bubble, pk=pk)
        bubble_post = get_object_or_404(CommunityChat, id=post_id)
        Bubble_id = bubble.id

        #list of reponses to bubble post
        responses = CommunityResponse.objects.filter(original_chat=bubble_post).order_by('created_on')

        post_data = [{
            "sender": response.user.user_id.username[:1],
            "sender_id": response.user.user_id.id,
            "message": response.message,
            "created_at": response.created_on.strftime("%Y-%m-%d %H:%M:%S"),
            "post_id": response.id
        } for response in responses]

        response = JsonResponse({"posts": post_data})
        response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
        response['Pragma'] = 'no-cache'
        response['Expires'] = '0'
        return response
    else:
        # Handle non-AJAX requests here
        pass

def post_post_response(request, pk, post_id):
    bubble = get_object_or_404(Bubble, pk=pk)
    bubble_post = get_object_or_404(CommunityChat, id=post_id)
    Bubble_id = bubble.id
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        form = BubblePostResponseForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = BubbleMember.objects.get(bubble_id=Bubble_id, user_id=request.user )
            post.original_chat = bubble_post
            post.save()
            return JsonResponse({'status': 'success', 'message': post.message })
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    return JsonResponse({'status': 'error', 'message': 'Invalid request'})


def swipe_view(request, target_user_id, action):
    current_user = request.user
    target_user = User.objects.get(pk=target_user_id)

    # Attempt to get an existing friend record in either user1/user2 combination
    try:
        friend = Friend.objects.get(
            (Q(user1=current_user) & Q(user2=target_user)) | 
            (Q(user1=target_user) & Q(user2=current_user))
        )
        created = False
    except Friend.DoesNotExist:
        # Create a new friend record if none exists
        friend = Friend(user1=current_user, user2=target_user, status1=Friend.PENDING, status2=Friend.PENDING)
        friend.save()
        created = True

    if friend.user1 == current_user:
    # Logic for swipe right
        if action == 'right':
            # If it's already pending, set to ACCEPTED, else set to PENDING
            if friend.status1 == Friend.PENDING:
                friend.status1 = Friend.ACCEPTED
            elif friend.status1 == Friend.DECLINED:
                friend.status1 = Friend.ACCEPTED
            friend.save()

        # Logic for swipe left
        elif action == 'left':
            # Set to DECLINED only if not already ACCEPTED
            if friend.status1 == Friend.PENDING:
                friend.status1 = Friend.DECLINED
            if friend.status1 == Friend.ACCEPTED:
                friend.status1 = Friend.DECLINED
                friend.save()

    elif friend.user2 == current_user:
            # Logic for swipe right
        if action == 'right':
            # If it's already pending, set to ACCEPTED, else set to PENDING
            if friend.status2 == Friend.PENDING:
                friend.status2 = Friend.ACCEPTED
            elif friend.status2 == Friend.DECLINED:
                friend.status2 = Friend.ACCEPTED
            friend.save()

        # Logic for swipe left
        elif action == 'left':
            # Set to DECLINED only if not already ACCEPTED
            if friend.status2 == Friend.PENDING:
                friend.status2 = Friend.DECLINED
            elif friend.status2 == Friend.ACCEPTED:
                friend.status2 = Friend.DECLINED
                friend.save()

    return JsonResponse({'status': 'success'})

from .models import EntryTest
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def test_view(request, test_id):
    test = get_object_or_404(EntryTest, id=test_id)
    questions = test.questions.all()
    paginator = Paginator(questions, 1)  # 1 question per page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'core/test.html', {
        'test': test,
        'page_obj': page_obj,
    })

from django.http import JsonResponse
from .models import OptionResponse, Option, Question
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def update_option_response(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        option_id = request.POST.get('option_id')  # This is actually the option name
        tick = request.POST.get('tick') == 'true'
        question_id = request.POST.get('question_id')
        entry_test_id = request.POST.get('entry_test_id')

        # Retrieve the actual objects based on the provided identifiers
        user = get_object_or_404(User, pk=user_id)
        option = get_object_or_404(Option, pk=option_id)  # Assuming 'name' is the unique identifier
        question = get_object_or_404(Question, pk=question_id)
        entry_test = get_object_or_404(EntryTest, pk=entry_test_id)

        obj, created = OptionResponse.objects.update_or_create(
            user=user, option=option, question=question, EntryTest=entry_test,
            defaults={'tick': tick}
        )
        return JsonResponse({'success': True, 'created': created})
    return JsonResponse({'success': False}, status=400)



from .models import Answer, Question, EntryTest
from .forms import AnswerForm

@csrf_exempt
def answer_question(request):
    if request.method == 'POST':
        user = request.user
        question_id = request.POST.get('question_id')
        entrytest_id = request.POST.get('entrytest_id')
        text = request.POST.get('text')

        question = get_object_or_404(Question, pk=question_id)
        entry_test = get_object_or_404(EntryTest, pk=entrytest_id)

        answer, created = Answer.objects.get_or_create(
            user=user, question=question, EntryTest=entry_test,
            defaults={'text': text}
        )
        if not created:
            answer.text = text
            answer.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

from core.models import EntryTestSubmit

@login_required
def submit_entry_test(request, entry_test_id):
    user = request.user
    entry_test = EntryTest.objects.get(id=entry_test_id)
    
    if request.method == 'POST':
        # This will either create a new instance or get the existing one
        # This will either create a new instance or get the existing one
        test_submit, created = EntryTestSubmit.objects.get_or_create(
            user=user, 
            entryTest=entry_test
        )

        # Set Submit to True regardless of whether the object was just created
        test_submit.Submit = True
        test_submit.save()


        return redirect('/')  # Redirect to the home page

    return redirect('/')


from .models import MessageNotification

@login_required
def get_message_count(request, sender_id):
    receiver = request.user
    try:
        notification = MessageNotification.objects.get(receiver=receiver, sender_id=sender_id)
    except MessageNotification.DoesNotExist:
        notification = MessageNotification.objects.create(receiver=receiver, sender_id=sender_id)

    return JsonResponse({'unread_count': notification.unread_count})

@login_required
def reset_message_count(request, sender_id):
    receiver = request.user
    MessageNotification.objects.filter(receiver=receiver, sender_id=sender_id).update(unread_count=0)
    return JsonResponse({'status': 'success'})


from core.models import BubbleMessageNotification

@login_required
def get_bubble_message_count(request, sender_id, pk):
    receiver = request.user
    bubble = Bubble.objects.get(pk=pk)
    try:
        notification = BubbleMessageNotification.objects.get(bubble=bubble, receiver=receiver, sender_id=sender_id)
    except BubbleMessageNotification.DoesNotExist:
        notification = BubbleMessageNotification.objects.create(bubble=bubble, receiver=receiver, sender_id=sender_id)

    return JsonResponse({'unread_count': notification.unread_count})

@login_required
def reset_bubble_message_count(request, sender_id, pk):
    receiver = request.user
    BubbleMessageNotification.objects.filter(receiver=receiver, sender_id=sender_id, bubble=pk).update(unread_count=0)
    return JsonResponse({'status': 'success'})


from datetime import timedelta
from django.utils import timezone
from .task import Switch_voting

def bubbleTimerStart(request, pk):
    # Schedule the task to run in 48 hours
    Switch_voting.apply_async((pk,), eta=timezone.now() + timedelta(hours=48))
