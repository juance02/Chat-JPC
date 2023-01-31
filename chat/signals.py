from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import perfil
from django.dispatch import receiver

@receiver(post_save, sender=User)
def create_perfil(sender, instance, created, **kwargs):
    if created:
        perfil.objects.create(user=instance)