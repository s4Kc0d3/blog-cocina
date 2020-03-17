from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse

from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout as do_logout

from .models import Post
from .forms import PostForm

# Create your views here.
def post_list(request):
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    return render(request, 'blog/index.html',{'posts': posts})


def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('index')
    else:
        form = PostForm()
    return render(request, 'blog/post_new.html', {'form': form})


def delete_post(request, post_id=None):
    post_to_delete = Post.objects.get(id=post_id)
    post_to_delete.delete()
    return redirect('index')


def edit_post(request, post_id=None):
    post = Post.objects.get(id=post_id)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('contenido_id', post_id=post.id)
            #return redirect('index') #, pk=post.pk)
    else:
        form = PostForm(instance=post)
        return render(request, 'blog/edit_post.html', {'form': form})


def contenido_id(request, post_id):
    post = Post.objects.get(id=post_id)
    if post:
        return render(request, 'blog/post_detail.html', {'post_id': post})
    else:
        return HttpResponse("No hay datos modificados")


def busqueda_productos(request):
    return render(request, "blog/buscar.html")


def buscar(request):
    product = request.GET['prd']
    if product:
        #mensaje = f"Artículo buscado: {request.GET['prd']}"
        listado = Post.objects.filter(title__contains=product)
        if listado:
            return render(request, "blog/resultados_busqueda.html", {"listado": listado, "query": product})

    return HttpResponse(f"No se a encontrado: {product}")

'''
Descripcion:
    Aqui debajo irán las funciones para controlar los logeo de usuarios

'''

def welcome(request):
    # Si estamos identificados devolvemos la portada
    if request.user.is_authenticated:
        return render(request, "users/welcome.html")
    # En otro caso redireccionamos al login    
    return render(request, "users/welcome.html")


def register(request):
    # Creamos el formulario de autenticación vacío
    form = UserCreationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = UserCreationForm(data=request.POST)
        # Si el formulario es válido...
        if form.is_valid():

            # Creamos la nueva cuenta de usuario
            user = form.save()

            # Si el usuario se crea correctamente 
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/register.html", {'form': form})


def login(request):
    # Creamos el formulario de autenticación vacío
    form = AuthenticationForm()
    if request.method == "POST":
        # Añadimos los datos recibidos al formulario
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Recuperamos las credenciales validadas
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            # Verificamos las credenciales del usuario
            user = authenticate(username=username, password=password)

            # Si existe un usuario con ese nombre y contraseña
            if user is not None:
                # Hacemos el login manualmente
                do_login(request, user)
                # Y le redireccionamos a la portada
                return redirect('/')

    # Si llegamos al final renderizamos el formulario
    return render(request, "users/login.html",{'form': form})


def logout(request):
    do_logout(request)
    # Redireccionamos a la portada
    return redirect('/')