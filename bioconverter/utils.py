import io

import numpy as np
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from bioconverter.models import ConversionRequest
from filterbank.models import ParsingRequest, Representation, AImage


@database_sync_to_async
def get_conversionrequest_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = ConversionRequest.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("ParsingRequest {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def get_inputmodel_or_error(model,pk):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    print(pk)
    print(model)
    inputmodel = model.objects.get(pk=pk)
    if inputmodel is None:
        raise ClientError("Inputmodel {0} does not exist".format(str(pk)))
    return inputmodel



@database_sync_to_async
def update_outputrepresentation_or_create(request: ConversionRequest, numpyarray):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.outputvid).first()
    if outputrep is None:
        #TODO make creation of outputvid
        outputrep = Representation.objects.create(name="RANDOM",creator=request.user,vid=request.outputvid,sample=request.sample,numpy=numpyarray)
    elif outputrep is not None:
        #TODO: update array of output
        outputrep.nparray.set_array(numpyarray)
    return outputrep

@database_sync_to_async
def update_image_onoutputrepresentation_or_error(request: ConversionRequest, original_image, path):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.outputvid).first()
    if outputrep is None:
        #TODO make creation of outputvid
        raise ClientError("VID {0} does not exist on Sample {1}".format(str(request.outputvid), request.sample))
    elif outputrep is not None:
        #TODO: update array of output
        img_io = io.BytesIO()
        original_image.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        if outputrep.image is None:
            outputrep.image = AImage()
            outputrep.image.save()

        outputrep.image.image = thumb_file
        outputrep.image.save()
        outputrep.save()
        print("YES")
    return outputrep

class ClientError(Exception):
    """
    Custom exception class that is caught by the websocket receive()
    handler and translated into a send back to the client.
    """
    def __init__(self, code):
        super().__init__(code)
        self.code = code