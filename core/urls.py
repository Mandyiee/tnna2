from django.urls import path 
from . import views

urlpatterns = [
    path('', views.index,name='index'),
    path('profile', views.profile,name='profile'),
    path('api', views.apiIndex,name='apiIndex'),
    path('admins/api/admins', views.apiAdmin,name='apiAdmin'),
]
