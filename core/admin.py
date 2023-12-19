from django.contrib import admin
from .models import CommunityChat, CommunityResponse, Profile, Bubble, BubbleMember, Friend, Message, Bubblemate_chat, ProfileTag, EntryTestSubmit


admin.site.register(CommunityChat)
admin.site.register(CommunityResponse)
admin.site.register(Profile)
admin.site.register(Bubble)
admin.site.register(BubbleMember)
admin.site.register(Friend)
admin.site.register(Message)
admin.site.register(Bubblemate_chat)
admin.site.register(ProfileTag)
admin.site.register(EntryTestSubmit)

from .models import EntryTest, Question, Option, OptionResponse, Answer, MessageNotification, BubbleMessageNotification, BubblePostResponseNotification

@admin.register(EntryTest)
class EntryTestAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')
    list_filter = ('state',)
    search_fields = ('name',)
    filter_horizontal = ('questions',)

class OptionInline(admin.TabularInline):
    model = Question.choices.through
    extra = 1

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('text',)
    inlines = [OptionInline]


@admin.register(Option)
class OptionAdmin(admin.ModelAdmin):
    list_display = ('text',)


@admin.register(OptionResponse)
class OptionResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'option', 'tick', 'question')
    list_filter = ('user', 'EntryTest')
    search_fields = ('user__username', 'option__text')

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('text', 'user', 'question')
    list_filter = ('user', 'EntryTest')
    search_fields = ('text', 'user__username', 'question__text')

@admin.register(MessageNotification)
class MessageNotificationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'sender', 'unread_count')
    list_filter = ('sender',)

@admin.register(BubbleMessageNotification)
class BubbleMessageNotificationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'sender', 'unread_count', 'bubble',)
    list_filter = ('sender','bubble',)

@admin.register(BubblePostResponseNotification)
class BubblePostResponseNotificationAdmin(admin.ModelAdmin):
    list_display = ('receiver', 'post', 'unread_count', 'bubble',)
    list_filter = ('bubble','post',)