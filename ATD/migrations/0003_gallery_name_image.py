# Generated by Django 4.2.1 on 2023-06-05 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ATD', '0002_gallery_segmentada'),
    ]

    operations = [
        migrations.AddField(
            model_name='gallery',
            name='name_image',
            field=models.CharField(default='lengua.png', max_length=150),
            preserve_default=False,
        ),
    ]