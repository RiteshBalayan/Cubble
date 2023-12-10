from django.db import models
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.utils import timezone

class Bubble(models.Model):

    class Status(models.TextChoices):
        ACT = "1", "ACTIVE"
        VOTE = '2', "VOTING"
        ARCH = '3', "ARCHIVE"

    name = models.CharField(max_length = 150, unique=True)
    description = models.CharField(max_length=500)
    thumbnail = models.ImageField(upload_to='Images')
    status = models.CharField(max_length = 10, choices=Status.choices, default = Status.ARCH)

    def __str__(self):
        return self.name

class BubbleMember(models.Model):

    class Status(models.TextChoices):
        SEE = "1", "VISIBLE"
        UNSEE = '2', "NOT_VISIBLE"

    bubble_id = models.ForeignKey(Bubble, related_name='bubble_registered_name', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, related_name='bubble_member', on_delete=models.CASCADE)
    profile = models.CharField(max_length = 500, blank=True)
    status = models.CharField(max_length = 10, choices=Status.choices, default = Status.UNSEE)

    class Meta:
        # Define unique constraint to ensure a user can join a bubble only once
        unique_together = ('bubble_id', 'user_id')

    def __str__(self):
        return f"Bubble ({self.bubble_id.name }) Profile of {self.user_id.username}"

class ProfileTag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Profile(models.Model):

    user_id = models.OneToOneField(User, related_name='Profile', on_delete=models.CASCADE)
    description = models.CharField(max_length = 500, blank=True)
    interests = models.ManyToManyField(ProfileTag, blank=True)
    profile_pic = models.ImageField(upload_to='profil_pic', blank=True)

    def __str__(self):
        return f"Profile of {self.user_id.username}"

class CommunityChat(models.Model):

    bubble_id = models.ForeignKey(Bubble, related_name='bubble_chat', on_delete=models.CASCADE)
    user = models.ForeignKey(BubbleMember, related_name='chatter', on_delete=models.CASCADE)
    title = models.CharField(max_length = 100)
    message = models.CharField(max_length = 500)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} #{self.id}"
    
    

class CommunityResponse(models.Model):

    original_chat = models.ForeignKey(CommunityChat, on_delete=models.CASCADE)
    user = models.ForeignKey(BubbleMember, related_name='chatter_small', on_delete=models.CASCADE)
    message = models.CharField(max_length = 500)
    created_on = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.user_id.username} responce #{self.id} to ({self.original_chat.title})"


class Friend(models.Model):
    PENDING = 'pending'
    ACCEPTED = 'accepted'
    DECLINED = 'declined'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (ACCEPTED, 'Accepted'),
        (DECLINED, 'Declined'),
    ]
    user1 = models.ForeignKey(User, related_name='friendship_user1', on_delete=models.CASCADE)
    user2 = models.ForeignKey(User, related_name='friendship_user2', on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    status1 = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)
    status2 = models.CharField(max_length=10, choices=STATUS_CHOICES, default=PENDING)

    # You might want to add more fields related to the friendship, such as when it was established
    
    class Meta:
        unique_together = ['user1', 'user2']

    def __str__(self):
        return f"{self.user1.username} - {self.user2.username} Friendship"

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    chat = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username} at {self.created_at}"

class Bubblemate_chat(models.Model):
    bubble_id = models.ForeignKey(Bubble, related_name='bubble_mate_chat', on_delete=models.CASCADE)
    sender = models.ForeignKey(BubbleMember, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(BubbleMember, related_name='received_messages', on_delete=models.CASCADE)
    chat = models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.user_id.username} to {self.receiver.user_id.username} at {self.created_at}"


class EntryTest(models.Model):
    STATE_CHOICES = [('active', 'Active'), ('archive', 'Archive')]
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=7, choices=STATE_CHOICES, default='archive')
    questions = models.ManyToManyField('Question', related_name='tests')

    def __str__(self):
        return f"{self.name}"

class Question(models.Model):
    text = models.TextField()
    choices = models.ManyToManyField('Option', blank=True)

    def __str__(self):
        return f"{self.text}"


class Option(models.Model):
    text = models.TextField()

    def __str__(self):
        return f"{self.text}"

class OptionResponse(models.Model):
    tick = models.BooleanField(blank=True)
    user = models.ForeignKey(User, related_name='user', on_delete=models.CASCADE)
    option = models.ForeignKey(Option, related_name='OptionResponce_option', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='OptionResponce_question', on_delete=models.CASCADE, null=True)
    EntryTest = models.ForeignKey(EntryTest, related_name='OptionResponce_entrytest', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user} responce to {self.EntryTest} | {self.question} | {self.option} "

class Answer(models.Model):
    text = models.TextField(blank=True)
    user = models.ForeignKey(User, related_name='answer', on_delete=models.CASCADE)
    question = models.ForeignKey(Question, related_name='Answer_question', on_delete=models.CASCADE , null=True)
    EntryTest = models.ForeignKey(EntryTest, related_name='Answer_entrytest', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f"{self.user} responce to {self.EntryTest} | {self.question}"

