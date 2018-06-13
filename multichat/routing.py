from django.urls import path
from rest_framework.authentication import BasicAuthentication
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack

from chat.authentification_helper import QueryAuthMiddleware
from chat.consumers import ChatConsumer, PrintConsumer, CommentConsumer

OauthMiddleWareStack = lambda inner: QueryAuthMiddleware(AuthMiddlewareStack(inner))

# The channel routing defines what connections get handled by what consumers,
# selecting on either the connection type (ProtocolTypeRouter) or properties
# of the connection's scope (like URLRouter, which looks at scope["path"])
# For more, see http://channels.readthedocs.io/en/latest/topics/routing.html
application = ProtocolTypeRouter({

    # Channels will do this for you automatically. It's included here as an example.
    # "http": AsgiHandler,

    # Route all WebSocket requests to our custom chat handler.
    # We actually don't need the URLRouter here, but we've put it in for
    # illustration. Also note the inclusion of the AuthMiddlewareStack to
    # add users and sessions - see http://channels.readthedocs.io/en/latest/topics/authentication.html
    "websocket": QueryAuthMiddleware(
        URLRouter([
            # URLRouter just takes standard Django path() or url() entries.
            path("chat/stream/", ChatConsumer),
            path("comments/stream/", CommentConsumer)
        ]),
    ),
    "channel": ChannelNameRouter({
        "print": PrintConsumer,
    }),
})
