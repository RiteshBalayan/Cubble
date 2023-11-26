from django.contrib.auth.models import User
from functools import wraps
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from core.models import BubbleMember, Bubble, Friend
from django.http import HttpResponseForbidden
from django.db.models import Q

def part_of_bubble_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        bubble_id = kwargs.get('pk')  # Get pk from URL parameters
        bubble = get_object_or_404(Bubble, id=bubble_id)

        # Check if the user is logged in
        if not request.user.is_authenticated:
            return login_required(view_func)(request, *args, **kwargs)

        user_id = request.user.id
        bubble_member = BubbleMember.objects.filter(bubble_id=bubble_id, user_id=user_id).exists()

        # Check if the user is part of the bubble
        if bubble_member:
            return view_func(request, *args, **kwargs)
        else:
            # You can customize the behavior for unauthorized users here
            # For example, redirect to another page or return a forbidden response
            return HttpResponseForbidden("You are not a member of this bubble")

    return wrapped_view


def friend_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        friend_username = kwargs.get('friend_username')  # Get username from URL parameters
        friend = get_object_or_404(User, username=friend_username)
        friend_user_id = friend

        # Check if the user is logged in
        if not request.user.is_authenticated:
            return login_required(view_func)(request, *args, **kwargs)

        user_id = request.user
        friendship = Friend.objects.filter(Q(user1=user_id, user2=friend_user_id) | Q(user1=friend_user_id,user2=user_id)).exists()
        
        # Check if the user is part of the bubble
        if friendship:
            return view_func(request, *args, **kwargs)
        else:
            # You can customize the behavior for unauthorized users here
            # For example, redirect to another page or return a forbidden response
            return HttpResponseForbidden("You are not a friend with user")

    return wrapped_view