import base64
from PIL import Image as ImagePIL
from io import BytesIO
from os.path import basename, join
from urllib.parse import urlparse
from urllib.request import urlopen
from http import HTTPStatus

from django.urls import reverse
from django.test import TestCase
from django.conf import settings

from django.core.files.images import ImageFile
from .models import Image
from .forms import ImageUploadForm, ImageChangeSize

# Create your tests here.


class ImageTestCase(TestCase):
    url = 'https://images2.minutemediacdn.com/image/upload/' \
          'c_crop,h_1193,w_2121,x_0,y_64/' \
          'f_auto,q_auto,w_1100/v1565279671/' \
          'shape/mentalfloss/' \
          '578211-gettyimages-542930526.jpg'
    path = join(
        settings.BASE_DIR,
        'images',
        'test_images',
        '_118158924_gettyimages-507245091.jpg'
    )
    path_2 = join(
        settings.BASE_DIR,
        'images',
        'test_images',
        'testing.jpg'
    )

    def setUp(self):
        Image.objects.create(
            file=ImageFile(
                BytesIO(urlopen(self.url).read()),
                urlparse(self.url).path.split('/')[-1],
            )
        )
        with open(self.path, 'rb') as file:
            Image.objects.create(
                file=ImageFile(
                    file,
                    basename(self.path),
                )
            )

    def test_file_ext(self):
        image = Image.objects.last()
        self.assertEqual(
            image.file_ext(),
            'jpeg'
        )

    def test_get_image(self):
        image = Image.objects.last()
        image_no_resize = ImagePIL.open(
            BytesIO(base64.b64decode(image.get_image()))
        )
        image_resize_w = ImagePIL.open(
            BytesIO(
                base64.b64decode(
                    image.get_image(width=100)
                )
            )
        )
        image_resize_h = ImagePIL.open(
            BytesIO(
                base64.b64decode(
                    image.get_image(height=100)
                )
            )
        )
        self.assertEqual(
            image_no_resize.width,
            image.file.width
        )
        self.assertEqual(
            image_no_resize.height,
            image.file.height
        )
        self.assertEqual(
            image_resize_w.width,
            100
        )
        self.assertNotEqual(
            image_resize_w.height,
            image.file.height
        )
        self.assertEqual(
            image_resize_h.height,
            100
        )
        self.assertNotEqual(
            image_resize_w.width,
            image.file.width
        )

    def test_list_view(self):
        resp = self.client.get(
            '/'
        )
        self.assertEqual(
            resp.status_code, HTTPStatus.OK
        )

    def test_detail_view(self):
        image = Image.objects.last()
        resp = self.client.get(
            reverse(
                'image_change',
                kwargs={
                    'pk': image.pk
                }
            )
        )
        self.assertEqual(
            resp.status_code, HTTPStatus.OK
        )

    def test_create_view(self):
        resp = self.client.get(
            reverse('image_create')
        )

        self.assertEqual(
            resp.status_code, HTTPStatus.OK
        )
        with open(self.path, 'rb') as file:
            resp = self.client.post(
                reverse('image_create'),
                {'file': file}
            )
            import pdb;pdb.set_trace()
            self.assertEqual(resp.status_code, HTTPStatus.OK)
            self.assertTrue(
                Image.objects.get(
                    file__name=basename(self.path_2)
                )
            )
