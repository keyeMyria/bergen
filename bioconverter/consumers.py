import javabridge as javabridge
import bioformats
import numpy as np
from channels.consumer import AsyncConsumer

from bioconverter.models import ConversionRequest
from bioconverter.utils import get_inputmodel_or_error, get_conversionrequest_or_error
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

    async def toimage(self, request, array):
        # TODO: Maybe faktor this one out
        img = toimage(array)

        path = "sample_{0}_vid_{1}".format(str(request.sample.pk), str(request.outputvid))
        outputrep: Representation = await update_image_onoutputrepresentation_or_error(request,img,path)

        returnchannel = "sample_{0}".format(str(request.sample.pk))
        serializer = RepresentationSerializer(instance=outputrep)
        stream = "representations"
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


javabridge.start_vm(class_path=bioformats.JARS, run_headless=True)

class BioConverter(ConverterConsumer):
    async def convert(self, conversionsettings: dict, inputmodel: BioImage) -> np.array:
        filepath = inputmodel.file.path

        meta, array = loadSeriesFromFile(filepath, conversionsettings["series"])

        return array
