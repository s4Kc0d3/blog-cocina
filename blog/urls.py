from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='index'),
    path('post/new', views.post_new, name='post_new'),
    path('delete/<post_id>', views.delete_post, name='delete_post'),
    path('edit/<post_id>', views.edit_post, name='edit_post'),
]
