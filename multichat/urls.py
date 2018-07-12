from django.conf.urls import url
from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.views import login, logout
from rest_framework import routers
from django.conf import settings
from django.conf.urls.static import static

import drawing.routes
import filterbank.routes
import social.routes
import bioconverter.routes
import biouploader.routes
from chat.views import index, test
from representations.views import TagAutocomplete

router = routers.DefaultRouter()
router.registry.extend(social.routes.router.registry)
router.registry.extend(drawing.routes.router.registry)
router.registry.extend(filterbank.routes.router.registry)
router.registry.extend(bioconverter.routes.router.registry)
router.registry.extend(biouploader.routes.router.registry)


urlpatterns = [
    path('', index),
    path('test', test),
    url(r'^accounts/', include('registration.backends.simple.urls')),
    path('admin/', admin.site.urls),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
    url(r'^api/', include((router.urls, 'api'))),
    url(r'^tags/$',TagAutocomplete.as_view(),name='tags'),
]

if settings.DEBUG is True:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
