from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

  

    path('home/', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('Gallery/', views.gallery, name='Gallery'),

    path('photo/<int:id>/', views.photo_detail, name='photo_detail'),

    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),

    path('gallery/download-all/', views.download_all_images, name='download_all'),

    path('live_preview/', views.live_preview, name='live_preview'),

     path('logout/', views.custom_logout, name='custom_logout'),
]