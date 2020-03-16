from django.shortcuts import render, redirect
from django.utils import timezone
from django.http import HttpResponse
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
        #return HttpResponse(post)
    else:
        return HttpResponse("No hay datos modificados")


def busqueda_productos(request):

    return render(request, "blog/buscar.html")


def buscar(request):

    mensaje = f"Artículo buscado: {request.GET['prd']}"

    return HttpResponse(mensaje)