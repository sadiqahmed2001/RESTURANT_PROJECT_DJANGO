from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post, TeamMember, Reservation, Testimonial, ContactForm, MenuItem, Cart, Order, Payment
from django.utils import timezone

class PostModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            slug='test-post',
            author=self.user,
            body='This is a test post.',
            publish=timezone.now(),
            status=Post.Status.DRAFT
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.author.username, 'testuser')
        self.assertEqual(self.post.status, 'DF')

class TeamMemberModelTest(TestCase):

    def setUp(self):
        self.team_member = TeamMember.objects.create(
            full_name='sadiq ahmed',
            designation='Developer',
            facebook_url='https://facebook.com/developer',
            twitter_url='https://twitter.com/developer',
            instagram_url='https://instagram.com/developer'
        )

    def test_team_member_creation(self):
        self.assertEqual(self.team_member.full_name, 'sadiq ahmed')
        self.assertEqual(self.team_member.designation, 'Developer')

class ReservationModelTest(TestCase):

    def setUp(self):
        self.reservation = Reservation.objects.create(
            name='sadiq ahmed',
            email='dadd@example.com',
            date_time=timezone.now(),
            num_people=4,
            special_request='Window seat',
            is_reserved=True
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.name, 'sadiq ahmed')
        self.assertEqual(self.reservation.email, 'dadd@example.com')

class TestimonialModelTest(TestCase):

    def setUp(self):
        self.testimonial = Testimonial.objects.create(
            name='Customer',
            profession='Engineer',
            testimonial='Great service!',
            rating=5
        )

    def test_testimonial_creation(self):
        self.assertEqual(self.testimonial.name, 'Customer')
        self.assertEqual(self.testimonial.rating, 5)

class ContactFormModelTest(TestCase):

    def setUp(self):
        self.contact_form = ContactForm.objects.create(
            name='Ali',
            phone='1234567890',
            email='ali@example.com',
            subject='Inquiry',
            message='I have a question.',
            is_solved=False
        )

    def test_contact_form_creation(self):
        self.assertEqual(self.contact_form.name, 'Ali')
        self.assertEqual(self.contact_form.subject, 'Inquiry')

class MenuItemModelTest(TestCase):

    def setUp(self):
        self.menu_item = MenuItem.objects.create(
            name='Burger',
            description='Tasty burger',
            price=5.99,
            category=2,
            type=2,
            is_available=True,
            is_vegetarian=False
        )

    def test_menu_item_creation(self):
        self.assertEqual(self.menu_item.name, 'Burger')
        self.assertEqual(self.menu_item.price, 5.99)

class CartModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.menu_item = MenuItem.objects.create(
            name='Burger',
            description='Tasty burger',
            price=5.99,
            category=2,
            type=2,
            is_available=True,
            is_vegetarian=False
        )
        self.cart = Cart.objects.create(
            userid=self.user,
            mid=self.menu_item,
            qty=3
        )

    def test_cart_creation(self):
        self.assertEqual(self.cart.userid.username, 'testuser')
        self.assertEqual(self.cart.qty, 3)
        self.assertEqual(self.cart.total_price, self.menu_item.price * 3)

class OrderModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.menu_item = MenuItem.objects.create(
            name='Burger',
            description='Tasty burger',
            price=5.99,
            category=2,
            type=2,
            is_available=True,
            is_vegetarian=False
        )
        self.order = Order.objects.create(
            order_id='ORDER123',
            user_id=self.user,
            m_id=self.menu_item,
            qty=2,
            amt=21.98,
            is_Paid=False,
            is_ready=False,
            update_desc='Test order description',
            timestamp=timezone.now()
        )

    def test_order_creation(self):
        self.assertEqual(self.order.order_id, 'ORDER123')
        self.assertEqual(self.order.user_id.username, 'testuser')
        self.assertEqual(self.order.m_id.name, 'Burger')
        self.assertEqual(self.order.qty, 2)
        self.assertEqual(self.order.amt, 21.98)
        self.assertFalse(self.order.is_Paid)
        self.assertFalse(self.order.is_ready)

class PaymentModelTest(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.menu_item = MenuItem.objects.create(
            name='Burger',
            description='Tasty burger',
            price=5.99,
            category=2,
            type=2,
            is_available=True,
            is_vegetarian=False
        )
        self.order = Order.objects.create(
            order_id='ORDER123',
            user_id=self.user,
            m_id=self.menu_item,
            qty=2,
            amt=21.98,
            is_Paid=False,
            is_ready=False,
            update_desc='Test order description',
            timestamp=timezone.now()
        )
        self.payment = Payment.objects.create(
            order=self.order,
            payment_id='PAYMENT123',
            payment_method='Credit Card',
            rozar_pay_order_id='RZP_ORDER_123',
            rozar_pay_Payment_id='RZP_PAYMENT_123',
            razorpay_signature='SIGNATURE123',
            amount=21.98,
            is_Paid=True
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.payment_id, 'PAYMENT123')
        self.assertEqual(self.payment.order.order_id, 'ORDER123')
        self.assertTrue(self.payment.is_Paid)
