from usuarios.models import *
from rest_framework import serializers
from chat.models import Message


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = Usuarios
        fields = ['nombreusuario', 'password']


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='nombreusuario', queryset=Usuarios.objects.all())
    receiver = serializers.SlugRelatedField(many=False, slug_field='nombreusuario', queryset=Usuarios.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
