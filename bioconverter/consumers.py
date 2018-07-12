import javabridge as javabridge
import bioformats
import numpy as np
import nibabel as nib
from channels.consumer import AsyncConsumer

from bioconverter.models import ConversionRequest, OutFlowRequest
from bioconverter.utils import get_inputmodel_or_error, get_conversionrequest_or_error, get_outflowrequest_or_error, \
    get_inputrepresentation_or_error, update_nifti_on_representation, update_image_on_representation
from biouploader.models import BioImage
from chat.logic.bioparser import loadSeriesFromFile
from filterbank.addins import toimage
from filterbank.models import Representation
from filterbank.serializers import RepresentationSerializer
from filterbank.utils import update_outputrepresentation_or_create, update_image_onoutputrepresentation_or_error


class ConverterConsumer(AsyncConsumer):

    async def startconverting(self, event):

        request: ConversionRequest = await get_conversionrequest_or_error(event["request"])

        #TODO: This is Still very Quick and Dirty but does the trick

        settings = {}
        defaultsettings = {}
        import json

        try:
            settings = json.loads(request.settings)
            try:
                defaultsettings = json.loads(request.converter.defaultsettings)
            except:
                defaultsettings = {}

        except:
            defaultsettings = {}
            settings = {}

        defaultsettings.update(settings)
        print(defaultsettings)
        inputmodel  = await self.getInputModel(request)
        #TODO: Implement parsing an array here

        convertedarray = await self.convert(settings,inputmodel)


        #TODO: Implement creating a Representation here

        outputrep: Representation = await update_outputrepresentation_or_create(request, numpyarray=convertedarray)

        path = "sample_{0}_vid_{1}".format(str(request.sample.pk),str(request.outputvid))
        print(path)
        stream = "representations"
        returnchannel = "sample_{0}".format(str(request.sample.pk))
        serializer = RepresentationSerializer(instance=outputrep)

        await self.channel_layer.group_send(
            returnchannel,
            {
                "type": "stream",
                "stream": stream,
                "room": returnchannel,
                "method": "put",
                "data": serializer.data
            }
        )
        # ASYNC PARSING OF THE IMAGE SUBCLASS

    async def convert(self, conversionsettings: dict, filepath) -> np.array:
        raise NotImplementedError

    async def getInputModel(self, request: ConversionRequest):
        model = await self.getModel(request)
        inputmodel = await get_inputmodel_or_error(model, str(request.inputid))
        return inputmodel


    async def getModel(self,request: ConversionRequest):
        #TODO: Implement a map of the available inputtypes and models
        type = request.converter.inputtype
        if type == "BioImage":
            print("returning bioimage")
            return BioImage
        else:
            raise Exception("Inputtype of Converter does not correlate with an existing Model")





class OutflowConsumer(AsyncConsumer):

    def __init__(self, scope):
        ''' This Class on bein consunmed will create a file coming from a representation:'''
        super().__init__(scope)

    async def startconverting(self, event):

        request: OutFlowRequest = await get_outflowrequest_or_error(event["request"])

        #TODO: This is Still very Quick and Dirty but does the trick

        settings = {}
        defaultsettings = {}
        import json

        try:
            settings = json.loads(request.settings)
            try:
                defaultsettings = json.loads(request.outflower.defaultsettings)
            except:
                defaultsettings = {}

        except:
            defaultsettings = {}
            settings = {}

        defaultsettings.update(settings)
        print(defaultsettings)
        inputrepresentation, array = await get_inputrepresentation_or_error(request)
        #TODO: Implement parsing an array here

        convertedarray = await self.convert(settings,array)

        outputrep: Representation = await self.callDatabasefunction(request, convertedarray)


        path = "sample_{0}_vid_{1}".format(str(request.sample.pk),str(request.inputvid))
        print(path)
        stream = "representations"
        returnchannel = "sample_{0}".format(str(request.sample.pk))
        serializer = RepresentationSerializer(instance=outputrep)

        await self.channel_layer.group_send(
            returnchannel,
            {
                "type": "stream",
                "stream": stream,
                "room": returnchannel,
                "method": "put",
                "data": serializer.data
            }
        )
        # ASYNC PARSING OF THE IMAGE SUBCLASS



    async def convert(self, conversionsettings: dict, array: np.array):
        raise NotImplementedError

    async def callDatabasefunction(self, request, convertedfile):
        raise NotImplementedError




class NiftiOutFlower(OutflowConsumer):

    async def convert(self, conversionsettings: dict, array):
        a = array
        a = np.interp(a, (a.min(), a.max()), (0, 256))
        array = a[:, :, :, :, 0]
        array = array.swapaxes(2, 3)
        print(array.max())
        test_stack = array.astype('u1')
        print(test_stack.mean())
        shape_3d = test_stack.shape[0:3]
        print(shape_3d)
        rgb_dtype = np.dtype([('R', 'u1'), ('G', 'u1'), ('B', 'u1')])
        nana = test_stack.copy().view(rgb_dtype).reshape(shape_3d)
        img1 = nib.Nifti1Image(nana, np.eye(4))
        return img1

    async def callDatabasefunction(self, request, convertedfile):
        return await update_nifti_on_representation(request, convertedfile)


class ImageOutFlower(OutflowConsumer):

    async def convert(self, conversionsettings: dict, array: np.array):
        # TODO: Maybe faktor this one out
        if len(array.shape) == 5:
            array = np.nanmax(array[:,:,:3,:,0], axis=3)
        if len(array.shape) == 4:
            array = np.nanmax(array[:,:,:3,:], axis=3)
        if len(array.shape) == 3:
            array = array[:,:,:3]
        print(array.shape)
        img = toimage(array)
        return img

    async def callDatabasefunction(self, request, convertedfile):
        return await update_image_on_representation(request, convertedfile)



javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)



class BioConverter(ConverterConsumer):
    async def convert(self, conversionsettings: dict, inputmodel: BioImage) -> np.array:
        filepath = inputmodel.file.path

        meta, array = loadSeriesFromFile(filepath, conversionsettings["series"])

        return array
