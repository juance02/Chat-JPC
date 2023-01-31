from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from chat.models import Message
from chat.forms import *
from chat.serializers import MessageSerializer, UserSerializer
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages 
from django.views.generic.base import View
from django.db.models import Q

def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'chat/index.html', {})
    if request.method == "POST":
        username, password = request.POST['username'], request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "User does not exist"}')
        return redirect('chats')



@csrf_exempt
def message_list(request, sender=None, receiver=None):
    """
    List all required messages, or create a new message.
    """
    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


""" def register_view(request):
    
    Render registration template
    
    if request.method == 'POST':
        print("working1")
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('chats')
    else:
        print("working2")
        form = SignUpForm()
    template = 'chat/register.html'
    context = {'form':form}
    return render(request, template, context) """

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request, user) 
            #messages.success(request, f'Usuario {username} creado')         
            return redirect('chats')
            
    else:
        form = UserCreationForm()

    return render(request, 'chat/register.html', {"form": form} )



def perfil(request, username=None):
    current_user = request.user
    if username and username !=current_user.username:
        user = User.objects.get(username=username)
        #product = user.product.all()

    else:
        #product = current_user.product.all()
        user = current_user
    return render(request, 'perfil/perfil.html', {'user':user,'perfil_list': User.objects.exclude(username=request.user.username)})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat/chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "chat/messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})



def editar_Perfil(request):
    if request.method == 'POST':
        u_formulario = UserUpdateForm(request.POST, instance=request.user)
        p_formulario = PerfilUpdateForm(request.POST, request.FILES, instance=request.user.perfil)
        if u_formulario.is_valid() and p_formulario.is_valid():
            u_formulario.save()
            p_formulario.save()
            return redirect('perfil')
            

    else:
        u_formulario = UserUpdateForm(instance=request.user)
        p_formulario = PerfilUpdateForm()
    context= {'u_formulario' : u_formulario, 'p_formulario':p_formulario}
    return render(request, 'perfil/crearPerfil.html', context)



def seguir(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user
    rel = seguidores(from_user=current_user, to_user=to_user_id)
    rel.save()
    messages.success(request, f'Has Comenzado a Seguir {username}')
    return redirect ('perfil')

def dejardeseguir(request, username):
    current_user = request.user
    to_user = User.objects.get(username=username)
    to_user_id = to_user.id
    rel = seguidores.objects.filter(from_user=current_user.id, to_user=to_user_id).get()
    rel.delete()
    messages.success(request, f'Dejaste de Seguir {username}')
    return redirect ('perfil')


def buscador (request):
    q=request.GET["q"]
    #productos=producto.objects.filter(activo=True,nombre__icontains=q)
    productos = User.objects.filter(username__icontains=q)
    #categorias = Categorias.objects.filter(activo=True)
    context = {'perfil':productos}
    return render(request, 'chat/usuarios.html' , context)

    #to_user = User.objects.get(username=username)
def usuarios (request, username):
    cat=User.objects.get(username=username)
    categorias=User.objects.filter(activo=True)
    productos=User.objects.filter(categorias=cat)
    context = {"productos":productos, "categorias":categorias}
    return render(request, 'chat/usuarios.html',context)


class UserSearch(View):
    def get (self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        perfil_list = User.objects.filter(Q(username__icontains=query))

        context = {
            'perfil_list':perfil_list,

        }
        return render(request, 'chat/usuarios.html', context)

    def chat_view(request):
        if not request.user.is_authenticated:
            return redirect('index')
        if request.method == "GET":
            return render(request, 'chat/chat.html',{'perfil_list': User.objects.exclude(username=request.user.username)})

    