import h5py
from django.db import models

from taggit.managers import TaggableManager
# Create your models here.
from drawing.models import Sample

class Experiment(models.Model):
    name = models.CharField(max_length=200)

    tags = TaggableManager()

    def __str__(self):
        return self.name