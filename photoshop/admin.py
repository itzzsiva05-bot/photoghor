from django.contrib import admin
from .models import Register, Photo, Category 
from .models import Gallery

class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id']

admin.site.register(Gallery, GalleryAdmin)

admin.site.register(Register)
admin.site.register(Photo)
admin.site.register(Category)
