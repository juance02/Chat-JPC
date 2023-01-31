from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path
from . import views
from chat.views import *


urlpatterns = [
    path('', views.index, name='index'),
    path('chat/', views.chat_view, name='chats'),
    path('chat/<int:sender>/<int:receiver>/', views.message_view, name='chat'),
    path('api/messages/<int:sender>/<int:receiver>/', views.message_list, name='message-detail'),
    path('api/messages/', views.message_list, name='message-list'),
    path('logout/', LogoutView.as_view(template_name='chat/index.html'), name='logout'),
    path('login/', LoginView.as_view(template_name='chat/Login.html'), name='login'),
    #path('logout/', logout, {'next_page': 'index'}, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/<str:username>/', views.perfil, name='perfil'),
    path('register/', views.register, name='register'),
    path('agregar-perfil/', views.editar_Perfil, name="agregar_Perfil"),
    path('seguir/<str:username>', views.seguir, name='seguir'),
    path('dejardeseguir/<str:username>', views.dejardeseguir, name='dejardeseguir'),
    
    path('usuarios/<str:username>/', views.usuarios, name="usuarios"),
    path('UserSearch/', UserSearch.as_view(), name="perfil-search"),
    path('UserSearch/<str:username>/', UserSearch.as_view(), name="perfil-search"),

]
