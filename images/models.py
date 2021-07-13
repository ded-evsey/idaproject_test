import os
import base64
import PIL
from io import BytesIO
from django.db import models
from django.urls import reverse
# Create your models here.


class Image(models.Model):
    file = models.ImageField('Файл', blank=True)
    upload = models.DateTimeField(
        'Дата и время добавления',
        auto_now_add=True
    )

    class Meta:
        ordering = ['upload']
        verbose_name = 'Изображение'
        verbose_name_plural = 'Изображения'

    def get_absolute_url(self):
        return reverse('image_change', args=(self.pk,))

    def filename(self):
        return self.file.name

    def file_ext(self):
        ext = self.filename().split('.')[1]
        return ext if ext != 'jpg' else 'jpeg'

    def resize_image(self, width=0, height=0):
        """
        resize first width, after height
        :param width:
        :param height:
        :return: bytes like object
        """
        size = [
            self.file.width,
            self.file.height
        ]
        if width and width != self.file.width:
            w_percent = width / size[0]
            size[0] = width
            size[1] = int(size[1] * w_percent)
        if height and height != self.file.height:
            h_percent = height / size[1]
            size[0] = int(size[0] * h_percent)
            size[1] = height
        with BytesIO() as f_object:
            image_pil = PIL.Image.open(self.file.path)
            image_pil = image_pil.resize(size)
            image_pil.save(f_object, self.file_ext())
            return f_object.getvalue()

    def get_image(self, width=0, height=0):
        if width or height:
            image = self.resize_image(width, height)
        else:
            image = self.file.file.read()
        return base64.b64encode(image).decode()
