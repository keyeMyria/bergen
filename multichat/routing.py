from django.urls import path
from channels.routing import ProtocolTypeRouter, URLRouter, ChannelNameRouter
from channels.auth import AuthMiddlewareStack

from bioconverter.consumers import BioConverter, NiftiOutFlower, ImageOutFlower
from filterbank.consumers import MaxISP
from trontheim.middleware import QueryAuthMiddleware
from chat.consumers import ChatConsumer
from trontheim.consumers import OsloConsumer

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
            path("oslo", OsloConsumer)
        ]),
    ),
    "channel": ChannelNameRouter({
        "maxisp": MaxISP,
        "bioconverter": BioConverter,
        "niftioutflower": NiftiOutFlower,
        "imageoutflower": ImageOutFlower,
    }),
})
