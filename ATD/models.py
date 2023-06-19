from django.db import models

# Create your models here.
class gallery(models.Model):
    image = models.ImageField()
    name_image = models.CharField(max_length=150)
    segmentada = models.CharField(max_length=100)
