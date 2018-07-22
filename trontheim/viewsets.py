from asgiref.sync import async_to_sync
from rest_framework import viewsets
from channels.layers import get_channel_layer
channel_layer = get_channel_layer()

class PublishingViewSet(viewsets.ModelViewSet):
    '''Enables publishing to the channel Layed.
    Publishers musst be Provided'''
    publishers = None

    def perform_create(self, serializer):
        super().perform_create(serializer)
        if self.publishers is not None:
            for el in self.publishers:
                try:
                    value = serializer.data[el]
                    path = "{0}_{1}".format(str(el), str(value))
                    print(path)
                    stream = str(serializer.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": "create", "data": serializer.data})
                except KeyError as e:
                    print("Publisher {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))

    def perform_update(self, serializer):
        super().perform_update(serializer)
        if self.publishers is not None:
            for el in self.publishers:
                try:
                    value = serializer.data[el]
                    path = "{0}_{1}".format(str(el), str(value))
                    print(path)
                    stream = str(serializer.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": "update", "data": serializer.data})
                except KeyError as e:
                    print("Publisher {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))

    def perform_destroy(self, instance):
        if self.publishers is not None:
            for el in self.publishers:
                try:
                    serialized = self.serializer_class(instance)
                    value = serialized.data[el]
                    path = "{0}_{1}".format(str(el), str(value))
                    print(path)
                    stream = str(self.serializer_class.Meta.model.__name__)
                    async_to_sync(channel_layer.group_send)(path, {"type": "stream", "stream": stream, "room": path,
                                                                   "method": "delete", "data": serialized.data})
                except KeyError as e:
                    print("Publisher {0} does not exist on {1}".format(str(el), str(self.serializer_class.__name__)))
        super().perform_destroy(instance)