from django.db import models

# Create your models here.
class Gallery(models.Model):
    image = models.ImageField(upload_to="original")
    name_image = models.CharField(max_length=150, null=True)
    name_segmentada = models.CharField(max_length=150, null=True)
    name_recortada = models.CharField(max_length=150, null=True)
    color_dominante = models.CharField(max_length=150, null=True)
    paleta_colores = models.CharField(max_length=150, null=True)
    saburra = models.CharField(max_length=150, null=True)
    textura = models.CharField(max_length=150, null=True)
    porcentaje = models.CharField(default="0.0 %", max_length=150)
    
    #segmentada = models.CharField(max_length=100)
