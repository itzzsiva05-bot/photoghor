import io
import os

from PIL import Image
from django.contrib import admin, messages
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.shortcuts import redirect
from django.urls import reverse

from .models import Category, Contact, Gallery, Photo, PhotoLike, Register, UserProfile


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def compress_image(image_file, max_mb=9):
    """
    Re-encode *image_file* as a progressive JPEG, reducing quality in steps
    until the result fits within *max_mb* megabytes (or quality reaches 10).
    """
    img = Image.open(image_file)
    if img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")

    output  = io.BytesIO()
    quality = 85

    while True:
        output.seek(0)
        output.truncate()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        size = output.seek(0, 2)
        output.seek(0)
        if size <= max_mb * 1024 * 1024 or quality <= 10:
            break
        quality -= 10

    filename = image_file.name.rsplit('.', 1)[0] + '.jpg'
    return InMemoryUploadedFile(
        output, 'ImageField', filename, 'image/jpeg', size, None
    )


# ---------------------------------------------------------------------------
# Admin registrations
# ---------------------------------------------------------------------------
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display  = ('name', 'email', 'subject', 'created_at')
    list_filter   = ('created_at',)
    search_fields = ('name', 'email', 'subject')
    readonly_fields = ('created_at',)
    ordering      = ('-created_at',)




@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'image', 'category']
    list_filter  = ['category']
    fields       = ['image', 'category']

    def add_view(self, request, form_url='', extra_context=None):
        if request.method == 'POST':
            files       = request.FILES.getlist('image')
            category_id = request.POST.get('category') or None
            if files:
                for f in files:
                    f.seek(0)
                    compressed = compress_image(f)
                    Gallery.objects.create(image=compressed, category_id=category_id)
                messages.success(request, f'{len(files)} image(s) uploaded successfully.')
                return redirect(reverse('admin:photoshop_gallery_changelist'))
        return super().add_view(request, form_url, extra_context)

    def save_model(self, request, obj, form, change):
        if obj.image:
            obj.image = compress_image(obj.image)
        super().save_model(request, obj, form, change)

    class Media:
        js = ('admin/js/gallery_multiple.js',)


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'created_at', 'likes_count')
    list_filter   = ('category',)
    search_fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        if 'image' in form.changed_data and obj.image:
            obj.image = compress_image(obj.image)
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name')
    search_fields = ('name',)





@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_letters', 'created_at')