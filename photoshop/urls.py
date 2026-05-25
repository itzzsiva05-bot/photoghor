from django.urls import path
from . import views

urlpatterns = [

    # ROOT URL
    path('', views.index, name='index'),

    

    path('home/', views.home, name='home'),

    path('register/', views.register, name='register'),

    path('photo/<int:id>/', views.photo_detail, name='photo_detail'),

    path('live-preview/', views.live_preview, name='live_preview'),

    path('logout/', views.logout_view, name='logout'),

    path('Gallery/', views.gallery, name='Gallery'),

    path("gallery/download-all/", views.download_all_images, name="download_all"),

    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),

]