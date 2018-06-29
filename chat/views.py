import numpy as np
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from filterbank.models import NpArray
from .models import Room


@login_required
def index(request):
    """
    Root page view. This is essentially a single-page app, if you ignore the
    login and admin parts.
    """
    # Get a list of rooms, ordered alphabetically
    rooms = Room.objects.order_by("title")

    # Render that in the index template
    return render(request, "index.html", {
        "rooms": rooms,
    })


def test(request):

    nana = NpArray.objects.create(filepath="nuni.h5",nparray=np.zeros((100,100,3)),position="nana")
    nana.save()

    nana.set_array(np.ones((100,100,4)))
    print(nana.get_array())

    return render(request, "index.html")
