from celery import shared_task
from .models import Bubble

@shared_task
def Switch_voting(pk):
    bubble = Bubble.objects.get(pk=pk)
    bubble.status = Bubble.Status.VOTE
    bubble.save()
