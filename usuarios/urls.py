from django.urls import path
from . import views 
from usuarios.views import *

urlpatterns = [
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path ('passwordolvidada/', views.passwordolvidada, name='passwordolvidada'), 
    path ('resetearpassword_validar/<uidb64>/<token>/', views.resetearpassword_validar, name='resetearpassword_validar'), 
    path ('resetearpassword/', views.resetearpassword, name='resetearpassword'), 
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('edit_perfil/', views.edit_perfil, name='edit_perfil'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/<str:nombreusuario>/', views.perfil, name='perfil'),
    path('seguir/<str:nombreusuario>/', views.seguir, name='seguir'),
    path('dejardeseguir/<str:nombreusuario>/', views.dejardeseguir, name='dejardeseguir'),
    path('usuarios/<str:nombres>/', views.usuarios, name="usuarios"),
    path('UserSearch/', UserSearch.as_view(), name="perfil-search"),
    path('UserSearch/<str:nombres>/', UserSearch.as_view(), name="perfil-search"),
    
 
      
]