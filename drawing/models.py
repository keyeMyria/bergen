from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Sample(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    location = models.CharField(max_length=100)
    name = models.CharField(max_length=100)

    def __str__(self):
        return "{0} by User: {1}".format(self.name,self.creator.username)

class ROI(models.Model):
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    vectors = models.CharField(max_length=3000)
    created_at = models.DateTimeField(auto_now=True)
    sample = models.ForeignKey(Sample,on_delete=models.CASCADE)

    def __str__(self):
        return "ROI created at {0} on Sample {1}".format(self.created_at.timestamp(),self.sample.name)