from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import path
from cubble_0_1 import consumers

websocket_urlpatterns = [
    path('ws/chat/<str:friend_username>/', consumers.ChatConsumer.as_asgi()),
]

application = ProtocolTypeRouter({
    'websocket': URLRouter(websocket_urlpatterns),
})
