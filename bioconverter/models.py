import os

from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from drawing.models import Sample

class BioImageFile(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(verbose_name="bioimage",upload_to="bioimagefiles")

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)

        super(BioImageFile, self).delete(*args, **kwargs)


class Converter(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=500)
    inputtype = models.CharField(max_length=200) #should contain a list of the model it can convert
    channel = models.CharField(max_length=100)
    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)

class OutFlower(models.Model):
    name = models.CharField(max_length=100)
    path = models.CharField(max_length=500)
    outputtype = models.CharField(max_length=200) #should contain a list of the model it can convert
    channel = models.CharField(max_length=100) # not the colour but the django channel
    defaultsettings = models.CharField(max_length=400) #json decoded standardsettings

    def __str__(self):
        return "{0} at Path {1}".format(self.name, self.path)


class ConversionRequest(models.Model):
    converter = models.ForeignKey(Converter, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The inputvid will pe parsed to the output vid (if no representation in that slot exists it will be created
    # otherwise just updated
    inputid = models.IntegerField() # the requested model which ought to be converted
    outputvid = models.IntegerField()

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.converter)

class OutFlowRequest(models.Model):
    outflower = models.ForeignKey(OutFlower, on_delete=models.CASCADE)
    sample = models.ForeignKey(Sample, on_delete=models.CASCADE)
    settings = models.CharField(max_length=1000) # jsondecoded
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The inputvid will pe parsed to the output vid (if no representation in that slot exists it will be created
    # otherwise just updated
    # The associated outputfile will be created on the respecting field in the model
    inputvid = models.IntegerField() # the requested model which ought to be converted

    def __str__(self):
        return "ConversionRequest for Converter: {0}".format(self.outflower)