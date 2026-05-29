from django.contrib import admin
from .models import Category, Photo, Gallery, PhotoLike, UserProfile, Register

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'category', 'created_at']
    list_filter = ['category']
    search_fields = ['title', 'description']

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']

@admin.register(PhotoLike)
class PhotoLikeAdmin(admin.ModelAdmin):
    list_display = ['user', 'photo', 'liked_date']

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'avatar_letters', 'created_at']

@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ['username', 'email']