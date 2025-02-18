from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Blog
from subscriber.models import Subscriber

@receiver(post_save, sender=Blog)
def send_blog_notification(sender, instance, created, **kwargs):
    if created and instance.author.is_superuser:  # Send only if the post is created & uploaded by admin
        subscribers = Subscriber.objects.all()
        recipient_list = [sub.email for sub in subscribers]

        if recipient_list:
            send_mail(
                subject=f"New Blog: {instance.title}",
                message=f"Hey, a new blog has been published: {instance.title}\n\nRead here: {instance.get_absolute_url()}",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=recipient_list,
                fail_silently=False,
            )
