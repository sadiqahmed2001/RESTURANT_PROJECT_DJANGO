from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'DF', 'Draft'
        PUBLISHED = 'PB', 'Published'

    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    status = models.CharField(max_length=2, choices=Status.choices, default=Status.DRAFT)

    class Meta:
        ordering = ['-publish']
        indexes = [
            models.Index(fields=['-publish']),
        ]

    def __str__(self):
        return self.title
    

class TeamMember(models.Model):
    full_name = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)
    image = models.ImageField(upload_to='team_images/', blank=True, null=True)
    facebook_url = models.URLField(blank=True, null=True)
    twitter_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.full_name


class Reservation(models.Model):
    user = models.ForeignKey(User,null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    date_time = models.DateTimeField()
    num_people = models.PositiveIntegerField()
    special_request = models.TextField(blank=True, null=True)
    is_reserved = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.date_time}"

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    profession = models.CharField(max_length=100)
    testimonial = models.TextField()
    rating = models.PositiveSmallIntegerField()
    image = models.ImageField(upload_to='testimonials/')

    def __str__(self):
        return self.name

class ContactForm(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    email = models.EmailField()
    subject = models.CharField(max_length=100)
    message = models.TextField()
    is_solved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

class MenuItem(models.Model):
    CAT = ((1, 'Breakfast'), (2, 'Lunch'), (3, 'Dinner'))
    TYP = ((1, 'Veg'), (2, 'Non-Veg'),(3,'HotDrinks'),(4,'ColdDrinks'))
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    category = models.IntegerField( choices=CAT, verbose_name="category")
    type = models.IntegerField( choices=TYP, verbose_name="type",default="")
    image = models.ImageField(upload_to='menu_items', null=True, blank=True)
    is_available = models.BooleanField(default=True, verbose_name="Is Available")
    is_vegetarian = models.BooleanField(default=False, verbose_name="Is Vegetarian")

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    userid = models.ForeignKey('auth.User', on_delete=models.CASCADE,db_column='userid')
    mid = models.ForeignKey(MenuItem, on_delete=models.CASCADE,db_column='mid')
    qty = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return self.mid.price * self.qty

    def __str__(self):
        return f"{self.mid.name} - {self.mid.name}"
    
class Order(models.Model):
    order_id = models.CharField(max_length=50)
    user_id = models.ForeignKey("auth.User", on_delete=models.CASCADE, db_column="user_id")
    m_id = models.ForeignKey(MenuItem, on_delete=models.CASCADE, db_column="m_id")
    qty = models.IntegerField(default=1)
    amt = models.FloatField(default=0.0)
    is_Paid = models.BooleanField(default=False)
    is_ready = models.BooleanField(default=False)
    update_desc= models.CharField(max_length=5000)
    timestamp= models.DateField(auto_now_add= True)

    def __str__(self):
        return self.update_desc[0:7] + "..."
    def __str__(self):
        return self.order_id

class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100)
    payment_method = models.CharField(max_length=50)
    rozarpay_order_id=models.CharField(max_length=100, null=True, blank=True)
    rozarpay_Payment_id=models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature=models.CharField(max_length=100, null=True, blank=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_Paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.payment_id
    
    

    

