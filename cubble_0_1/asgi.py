"""
ASGI config for cubble_0_1 project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
import cubble_0_1.routing  # replace 'your_app_name' with the name of your Django app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cubble_0_1.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            your_app_name.routing.websocket_urlpatterns
        )
    ),
})
