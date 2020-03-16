from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_list, name='index'),
    path('post/new', views.post_new, name='post_new'),
    path('delete/<post_id>', views.delete_post, name='delete_post'),
    path('edit/<post_id>', views.edit_post, name='edit_post'),
    path('busqueda_productos/', views.busqueda_productos),
    path('contenido/<post_id>', views.contenido_id, name='contenido_id'),
    path('buscar/', views.buscar),
    path('register/', views.register),
    path('login/', views.login),
    path('logout/', views.logout),
]
