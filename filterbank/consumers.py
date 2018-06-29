import javabridge as javabridge
import bioformats
import numpy as np
from channels.consumer import SyncConsumer, AsyncConsumer

from chat.logic.bioparser import loadBioMetaSeriesFromFile, loadBioImageSeriesFromFile
from filterbank.addins import toimage
from filterbank.models import ParsingRequest, Representation
from filterbank.serializers import RepresentationSerializer
from filterbank.utils import get_parsingrequest_or_error, get_inputrepresentation_or_error, \
    update_outputrepresentation_or_create, update_image_onoutputrepresentation_or_error


class FilterConsumer(AsyncConsumer):

    async def startparsing(self, event):

        request: ParsingRequest = await get_parsingrequest_or_error(event["request"])
        print(request)
        inputrep, array = await get_inputrepresentation_or_error(request)

        print(inputrep)
        #TODO: Implement parsing an array here

        parsedarray = await self.parse({"done":"hund"},array)


        #TODO: Implement creating a Representation here
        print(parsedarray)

        outputrep: Representation = await update_outputrepresentation_or_create(request, numpyarray=parsedarray)

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
        await self.toimage(request, array=array)

    async def parse(self, filtersettings: dict,numpyarray: np.array) -> np.array:
        raise NotImplementedError


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



class MaxISP(FilterConsumer):
    async def parse(self, filtersettings: dict, numpyarray: np.array) -> np.array:
        return np.random.random(numpyarray.shape)



class PrintConsumer(SyncConsumer):

    def __init__(self, scope):
        super().__init__(scope)

    def print(self, message):
        with javabridge.vm(run_headless=True, class_path=bioformats.JARS):
            meta = loadBioMetaSeriesFromFile("test.nd2", 0)
            image = loadBioImageSeriesFromFile("test.nd2", meta)

            print(image.shape)