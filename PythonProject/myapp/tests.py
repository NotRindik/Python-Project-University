from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import CustomUser, Listing, Message


class CustomUserTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='Zayka@gmail.com',
            password='TestPass123',
            first_name='Колян',
            last_name='Саниярович',
            phone='1234567890'
        )

    def test_user_creation(self):
        self.assertEqual(CustomUser.objects.count(), 1)
        self.assertEqual(self.user.email, 'Zayka@gmail.com')
        self.assertTrue(self.user.check_password('TestPass123'))

    def test_required_fields(self):
        with self.assertRaises(Exception):
            CustomUser.objects.create_user(email='missing@gmail.com', password='pass')

    def test_user_str(self):
        self.assertEqual(str(self.user), self.user.email)


class ListingTestCase(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='prodazhny@yandex.com',
            password='SellerPass123',
            first_name='Max',
            last_name='Maximov',
            phone='0987654321'
        )
        image_file = SimpleUploadedFile(
            name='test_image.jpg',
            content=b'\x47\x49\x46\x38\x89\x61',
            content_type='image/jpeg'
        )
        self.listing = Listing.objects.create(
            title='Test Item',
            description='Test Description',
            price=99.99,
            category='Electronics',
            location='Almaty',
            user=self.user,
            image=image_file
        )

    def test_listing_creation(self):
        self.assertEqual(Listing.objects.count(), 1)
        self.assertEqual(self.listing.title, 'Test Item')
        self.assertEqual(self.listing.user.email, 'prodazhny@yandex.com')

    def test_listing_str(self):
        self.assertEqual(str(self.listing), 'Test Item')

    def test_listing_timestamps(self):
        self.assertIsNotNone(self.listing.created_at)
        self.assertIsNotNone(self.listing.updated_at)


class MessageTestCase(TestCase):
    def setUp(self):
        self.sender = CustomUser.objects.create_user(
            email='otpravitel@iitu.edu.com',
            password='1234',
            first_name='DANILLAA',
            last_name='Kaltz',
            phone='1000000000'
        )
        self.recipient = CustomUser.objects.create_user(
            email='one@gmail.com',
            password='5678',
            first_name='One',
            last_name='Two',
            phone='2000000000'
        )
        self.message = Message.objects.create(
            sender=self.sender,
            recipient=self.recipient,
            content='Hello there!'
        )

    def test_message_creation(self):
        self.assertEqual(Message.objects.count(), 1)
        self.assertEqual(self.message.content, 'Hello there!')
        self.assertEqual(self.message.sender.email, 'otpravitel@iitu.edu.com')
        self.assertEqual(self.message.recipient.email, 'one@gmail.com')

    def test_message_str(self):
        self.assertIn('Message from', str(self.message))

class ListingViewTest(TestCase):
    def test_listing_page_status(self):
        response = self.client.get('/listing/')
        self.assertEqual(response.status_code, 200)


class ChatTest(TestCase):
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            email='user1@test.com',
            password='pass123',
            first_name='User1',
            last_name='Test',
            phone='1111111111',
            is_verified=True
        )
        self.user2 = CustomUser.objects.create_user(
            email='user2@test.com',
            password='pass123',
            first_name='User2',
            last_name='Test',
            phone='2222222222',
            is_verified=True
        )
        self.client.login(email='user1@test.com', password='pass123')


class AuthenticatedViewsTest(TestCase):

    def setUp(self):
        self.user = CustomUser.objects.create_user(
            email='test@example.com',
            password='testpass123',
            first_name='Kolya',
            last_name='Shishkin',
            phone='1234567890',
            is_verified=True
        )
        self.client.login(email='test@example.com', password='testpass123')

    def test_profile_page_context(self):
        response = self.client.get('/profile/')
        self.assertEqual(response.status_code, 200)

        def test_create_listing_post(self):
            image = SimpleUploadedFile(
                name='test_image.jpg',
                content=b'\x47\x49\x46\x38\x89\x61',
                content_type='image/jpeg'
            )

            response = self.client.post('/create/', {
                'title': 'New iPhone',
                'description': 'Brand new phone',
                'price': 999.99,
                'category': 'Electronics',
                'location': 'Almaty',
                'image': image
            })

            # Проверяем редирект после успешного создания
            self.assertEqual(response.status_code, 302)

            # Проверяем, что объявление появилось в БД
            new_listing = Listing.objects.get(title='New iPhone')
            self.assertEqual(new_listing.user, self.user)

            # Проверяем, что изображение сохранилось
            self.assertTrue(new_listing.image.name.endswith('test_image.jpg'))