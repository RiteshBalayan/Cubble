from django.contrib import admin
from .models import CommunityChat, CommunityResponse, Profile, Bubble, BubbleMember, Friend, Message, Bubblemate_chat, ProfileTag


admin.site.register(CommunityChat)
admin.site.register(CommunityResponse)
admin.site.register(Profile)
admin.site.register(Bubble)
admin.site.register(BubbleMember)
admin.site.register(Friend)
admin.site.register(Message)
admin.site.register(Bubblemate_chat)
admin.site.register(ProfileTag)
