from django.contrib.auth.models import User
from django.db import models


class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message = models.CharField(max_length=1200)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

    class Meta:
        ordering = ('timestamp',)

class seguidores(models.Model):
    from_user = models.ForeignKey(User, related_name='califi', on_delete=models.CASCADE)
    to_user = models.ForeignKey(User, related_name='califi_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user} '
    
    class Meta:
        indexes = [
        models.Index(fields=['from_user', 'to_user',]),
        ]


class perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image =models.ImageField(default='perfil.jfif')
    descripcion = models.TextField()

    def  __str__(self):
         return f'Perfil de {self.user.username}'

    def seguir(self):
        user_ids = seguidores.objects.filter(from_user=self.user)\
                                      .values_list('to_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)                              

    def dejardeseguir(self):
        user_ids = seguidores.objects.filter(to_user=self.user)\
                                      .values_list('from_user_id', flat=True)
        return User.objects.filter(id__in=user_ids)  





