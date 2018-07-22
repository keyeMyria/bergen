import os

from django.db import models

# Create your models here.
from drawing.models import Sample


class BioImage(models.Model):
    sample = models.ForeignKey(Sample,on_delete=models.CASCADE,blank=True,null=True,related_name='bioimages')
    name = models.CharField(max_length=100)
    file = models.FileField(verbose_name="bioimage",upload_to="bioimagefiles")

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if os.path.isfile(self.file.path):
            os.remove(self.file.path)

        super(BioImage, self).delete(*args, **kwargs)



