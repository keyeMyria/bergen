import io
import os

import nibabel as nib
import numpy as np
from channels.db import database_sync_to_async
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

from bioconverter.models import ConversionRequest, OutFlowRequest
from filterbank.models import ParsingRequest, Representation, AImage, Nifti
from multichat.settings import MEDIA_ROOT


@database_sync_to_async
def get_conversionrequest_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = ConversionRequest.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("ConversionRequest {0} does not exist".format(str(request["id"])))
    return parsing

@database_sync_to_async
def get_outflowrequest_or_error(request: dict):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    parsing = OutFlowRequest.objects.get(pk=request["id"])
    if parsing is None:
        raise ClientError("OutflowRequest {0} does not exist".format(str(request["id"])))
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
        raise ClientError("VID {0} does nots exist on Sample {1}".format(str(request.outputvid), request.sample))
    elif outputrep is not None:
        #TODO: update array of output
        img_io = io.BytesIO()
        original_image.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)

        if outputrep.image is None:
            outputrep.image = AImage()
            outputrep.image.save()

        model_image = AImage.objects.create(image=thumb_file)

        outputrep.image.image = thumb_file
        outputrep.image.save()
        outputrep.save()
        print("YES")
    return outputrep

@database_sync_to_async
def get_inputrepresentation_or_error(request: OutFlowRequest):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    inputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.inputvid).first()
    if inputrep.nparray is not None:
        array = inputrep.nparray.get_array()
    else:
        #TODO: This should never be called because every representation should have a nparray on creation
        print("ERROR ON INPUTREPRESENTATION")
        array = np.zeros((1024,1024,3))
    if inputrep is None:
        raise ClientError("Inputvid {0} does not exist on Sample {1}".format(str(request.inputvid), request.sample))
    return inputrep, array

@database_sync_to_async
def update_nifti_on_representation(request: OutFlowRequest, nifti):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.inputvid).first()
    if outputrep is None:
        #TODO make creation of outputvid
        raise ClientError("VID {0} does not exist on Sample {1}".format(str(request.inputvid), request.sample))
    elif outputrep is not None:
        #TODO: update array of output
        niftipath = "representation_nifti/sample_{0}_vid_{1}.nii.gz".format(request.sample_id, request.inputvid)
        niftipath = os.path.join(MEDIA_ROOT, niftipath)
        nib.save(nifti,niftipath)

        nifti = Nifti.objects.create(file=niftipath)
        outputrep.nifti = nifti
        outputrep.save()
        print("YES")
    return outputrep

@database_sync_to_async
def update_image_on_representation(request: OutFlowRequest, convertedfile):
    """
    Tries to fetch a room for the user, checking permissions along the way.
    """

    path = "sample_{0}_vid_{1}".format(str(request.sample.pk), str(request.inputvid))
    outputrep: Representation = Representation.objects.filter(sample=request.sample).filter(vid=request.inputvid).first()
    if outputrep is None:
        #TODO make creation of outputvid
        raise ClientError("VID {0} does nots exist on Sample {1}".format(str(request.inputvid), request.sample))
    elif outputrep is not None:
        #TODO: update array of output
        img_io = io.BytesIO()
        convertedfile.save(img_io, format='jpeg', quality=100)
        thumb_file = InMemoryUploadedFile(img_io, None, path + ".jpeg", 'image/jpeg',
                                          img_io.tell, None)



        model_image = AImage.objects.create(image=thumb_file)
        outputrep.image = model_image
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