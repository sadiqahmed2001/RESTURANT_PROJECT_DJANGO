from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .utils import send_notification_email

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        subject = 'Welcome to Our RESTURANT WEBSITE WE !!!'
        message = f'Thank you for registering, {instance.username}! 
        we are very glad to help you and provide you a world class services which is provided by our resturant
        thank you for your resturant!!!! :)--'
        send_notification_email(subject, message, [instance.email])
