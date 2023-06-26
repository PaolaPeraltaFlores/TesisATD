from django.db import models

# Create your models here.
class Gallery(models.Model):
    image = models.ImageField(upload_to="original")
    name_image = models.CharField(max_length=150)
    segmentada = models.CharField(max_length=100)
