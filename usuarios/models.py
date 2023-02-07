from dataclasses import fields
from distutils.command import upload
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

# Create your models here.

class UsuarioAdd(BaseUserManager):
    def create_user(self, nombres, apellidos, email, nombreusuario, password=None):
        if not email:
            raise ValueError('el usuario debe tener un email')

        if not nombreusuario:
            raise ValueError('el usuario debe tener nombreusuario')

        user = self.model(
            email = self.normalize_email(email),
            nombreusuario = nombreusuario,
            nombres = nombres,
            apellidos = apellidos,
        ) 

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, nombres, apellidos, email, nombreusuario, password):
        user = self.create_user(
            email = self.normalize_email(email),
            nombreusuario = nombreusuario,
            password = password,
            nombres = nombres,
            apellidos = apellidos, 
        ) 

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.save(using=self._db)
        return user


class Usuarios (AbstractBaseUser):
    nombres = models.CharField(max_length=50)
    apellidos = models.CharField(max_length=50)
    nombreusuario = models.CharField(max_length=50, unique=True)
    email = models.CharField(max_length=100, unique=True)
    numero_telefono = models.CharField(max_length=50)

    #campos atributos de django 

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombreusuario', 'nombres', 'apellidos']

    objects = UsuarioAdd()

    def full_nombre(self):
        return f'{self.nombres} {self.apellidos}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True

class seguidores(models.Model):
    from_user = models.ForeignKey(Usuarios, related_name='califi', on_delete=models.CASCADE)
    to_user = models.ForeignKey(Usuarios, related_name='califi_to', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.from_user} to {self.to_user} '
    
    class Meta:
        indexes = [
        models.Index(fields=['from_user', 'to_user',]),
        ]


class UserPerfil(models.Model):
    user = models.OneToOneField(Usuarios, on_delete=models.CASCADE)
    direccion_linea_1 = models.CharField(blank=True, max_length=100)
    direccion_linea_2 = models.CharField(blank=True, max_length=100)
    image_perfil = models.ImageField(upload_to='userperfil')
    ciudad = models.CharField(blank=True, max_length=20)
    departamento = models.CharField(blank=True, max_length=20)
    descripcion = models.TextField()

    def __str__(self):
        return self.user.nombres

    def full_direccion(self):
        return f'{self.direccion_linea_1} {self.direccion_linea_2}'

    def seguir(self):
        user_ids = seguidores.objects.filter(from_user=self.user)\
                                      .values_list('to_user_id', flat=True)
        return Usuarios.objects.filter(id__in=user_ids)                              

    def dejardeseguir(self):
        user_ids = seguidores.objects.filter(to_user=self.user)\
                                      .values_list('from_user_id', flat=True)
        return Usuarios.objects.filter(id__in=user_ids)  



