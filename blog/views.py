from django.shortcuts import render, redirect
from django.utils import timezone
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


def edit_post(request, post_Id=None):
    instance = Post.objects.get(id=post_id)
    form = PostForm(request.POST, instance=instance)
    
    if form.is_valid():
        instance = form.save(commit=False)
        instance.save()

    return render(request, "blog/edit_post.html", {'form': form})