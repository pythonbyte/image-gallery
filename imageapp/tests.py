from io import BytesIO
from PIL import Image

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.test import TestCase, Client
from django.urls import reverse

from .forms import PhotoForm
from .models import Photo

class TestFormImage(TestCase):

    def setUp(self):
        self.form_class = PhotoForm

        im = Image.new(mode='RGB', size=(200, 200))
        im_io = BytesIO()
        im.save(im_io, 'JPEG')
        im_io.seek(0)

        self.image = InMemoryUploadedFile(
            im_io, None, 'test.jpg', 'image/jpeg', len(im_io.getvalue()), None
        )

    def tearDown(self):
        del(self.image)

    def test_success_data(self):
        success_data = {
            'friends_name': 'john',
            'date_taken': '2019-09-25',

        }
        form = self.form_class(success_data, {'image_file': self.image})

        self.assertTrue(form.is_valid())

    def test_missing_file(self):
        data = {
            'friends_name': 'john',
            'date_taken': '2019-09-25',
        }
        form = self.form_class(data)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'image_file': ['This field is required.']})

    def test_invalid_file(self):
        im = Image.new(mode='RGB', size=(200, 200))
        im_io = BytesIO()
        im.save(im_io, 'PNG')
        im_io.seek(0)

        image = InMemoryUploadedFile(
            im_io, None, 'test.png', 'image/png', len(im_io.getvalue()), None
        )
        data = {
            'friends_name': 'john',
            'date_taken': '2019-09-25',
        }
        form = self.form_class(data, {'image_file': image})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'image_file': ['Incorrect type of image, only .JPG/.JPEG allowed.']})

    def test_missing_friends_name(self):
        data = {
            'date_taken': '2019-09-25',
        }
        form = self.form_class(data,  {'image_file': self.image})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'friends_name': ['This field is required.']})

    def test_numeric_friends_name(self):
        data = {
            'friends_name': '123456',
            'date_taken': '2019-09-25',
        }
        form = self.form_class(data,  {'image_file': self.image})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'friends_name': ['Invalid name. Please provide a valid one.']})

    def test_missing_date_taken(self):
        data = {
            'friends_name': 'john',
        }
        form = self.form_class(data,  {'image_file': self.image})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'date_taken': ['This field is required.']})

    def test_invalid_date_taken(self):
        data = {
            'friends_name': 'john',
            'date_taken': '2019-29-25'
        }
        form = self.form_class(data,  {'image_file': self.image})

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {'date_taken': ['Enter a valid date.']})


class TestPhotoEndpoints(TestCase):

    def setUp(self):
        self.client = Client()


    def test_get_list_photo_view(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_unauthorized_views(self):
        response = self.client.get('/approve-picture')
        response_approve = self.client.get('/approve-picture/1')
        response_delete = self.client.get('/delete-picture/1')

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response_approve.status_code, 302)
        self.assertEqual(response_delete.status_code, 302)

        self.assertEqual(response.url, '/login?next=/approve-picture')
        self.assertEqual(response_approve.url, '/login?next=/approve-picture/1')
        self.assertEqual(response_delete.url, '/login?next=/delete-picture/1')

    def test_like_photo(self):
        photo = Photo.objects.create(id=1, friends_name='test')
        response = self.client.post(
            reverse('imageapp:like-picture'),
            data={"image_id": photo.id},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        updated_photo = Photo.objects.get(id=1)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'image': 1, 'likes': 1})
        self.assertEqual(updated_photo.likes, 1)
        self.assertNotEqual(photo.likes, updated_photo.likes)

    def test_like_photo_not_ajax(self):
        photo = Photo.objects.create(id=2, friends_name='test')
        response = self.client.post(
            reverse('imageapp:like-picture'),
            data={"image_id": photo.id},
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Not allowed.'})

    def test_like_photo_not_exists(self):
        response = self.client.post(
            reverse('imageapp:like-picture'),
            data={"image_id": 3},
            HTTP_X_REQUESTED_WITH='XMLHttpRequest',
        )
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), {'error': 'Photo not found.'})
