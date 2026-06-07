from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('home/', views.home, name='home'),
    path('Gallery/', views.Gallery, name='Gallery'),  # ✓ gallery → Gallery
    path('photo/<int:id>/', views.photo_detail, name='photo_detail'),
    path('photo/<int:photo_id>/like/', views.like_photo, name='like_photo'),
    path('live_preview/', views.live_preview, name='live_preview'),
    path('logout/', views.custom_logout, name='custom_logout'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.contact, name='contact'),
    path('gallery/', views.gallery_view, name='gallery'),
]