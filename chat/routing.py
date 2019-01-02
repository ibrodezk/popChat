# chat/routing.py
from django.conf.urls import url

from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

from common.TwitchAuthenication import TwitchAuthenication
from . import consumers


# application = ProtocolTypeRouter({
#
#     "websocket": TwitchAuthenication(
#         URLRouter([
#             url(r"^chat/login/$", consumers.ChatConsumer),
#         ])
#     ),
#
# })
websocket_urlpatterns = [
    url(r'^ws/chat/room/(?P<room_name>[^/]+)/$', consumers.ChatConsumer),
]