from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('create_file/<str:name>/', views.create_file, name='create_file'),
    path('mkdir/<str:name>/', views.mkdir, name='mkdir'),
    path('list_dir_contents/', views.list_dir_contents, name='list_dir_contents'),
    path('delete_file/<str:name>/', views.delete_file, name='delete_file'),
    path('cd/<str:path>/', views.cd, name='cd'),
    path('append_to_file/<str:content>/', views.append_to_file, name='append_to_file'),
    path('truncate/', views.truncate, name='truncate'),
    path('mem_map/', views.mem_map, name='mem_map'),
    path('move/<str:name>/<str:dirname>/', views.move, name='move'),
]