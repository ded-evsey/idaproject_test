import os
from io import BytesIO, StringIO
from django.core.files.base import ContentFile
from django import forms
import PIL.Image
from urllib import request, parse
from .models import Image


class ImageUploadForm(forms.ModelForm):
    url = forms.URLField(required=False, label='Ссылка')

    class Meta:
        model = Image
        fields = ['file']

    def clean(self):
        cleaned_data = super().clean()
        url = cleaned_data.get('url')
        file = cleaned_data.get('file')
        if url and file:
            raise forms.ValidationError('Слишком много источников')
        if not url and not file:
            raise forms.ValidationError('Слишком мало источников')
        if url:
            res = request.urlopen(url)
            file_pil = PIL.Image.open(BytesIO(res.read()))
            filename = os.path.basename(parse.urlparse(url).path)
            ext = os.path.splitext(filename)[1].replace('.', '')
            f_object = BytesIO()
            file_pil.save(f_object, format=ext if ext != 'jpg' else 'jpeg')
            file = ContentFile(f_object.getvalue(), name=filename)
        cleaned_data['file'] = file
        self.save()
        return cleaned_data


class ImageChangeSize(forms.ModelForm):
    image_id = forms.ModelChoiceField(
        widget=forms.HiddenInput(),
        queryset=Image.objects.all(),
        initial=None
    )

    width = forms.IntegerField(label='Ширина', required=False)
    height = forms.IntegerField(label='Высота', required=False)

    class Meta:
        model = Image
        exclude = (
            'upload',
            'file'
        )
