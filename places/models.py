from django.db import models

from tinymce.models import HTMLField


class Place(models.Model):
    title = models.CharField('Название', max_length=200)
    description_short = models.TextField('Краткое описание', blank=True)
    description_long = HTMLField('Полное описание', blank=True)
    latitude = models.FloatField('Широта(lat)')
    longitude = models.FloatField('Долгота(lon)')

    def __str__(self):
        return self.title


class PlaceImage(models.Model):
    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name='Место'
        )
    image = models.ImageField('Изображение', upload_to='')
    position = models.PositiveIntegerField('Позиция', default=0, db_index=True)

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.position} - {self.place.title}"
