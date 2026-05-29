from django.contrib import admin
from .models import Register, Category, Photo, Gallery, PhotoLike, UserProfile
from PIL import Image
import io
from django.core.files.uploadedfile import InMemoryUploadedFile


def compress_image(image_file, max_mb=9):
    """Compress image to stay under Cloudinary's 10MB limit."""
    img = Image.open(image_file)

    # Convert RGBA/palette to RGB for JPEG compatibility
    if img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")

    output = io.BytesIO()
    quality = 85

    while True:
        output.seek(0)
        output.truncate()
        img.save(output, format="JPEG", quality=quality, optimize=True)
        size = output.tell()

        if size <= max_mb * 1024 * 1024 or quality <= 10:
            break
        quality -= 10

    output.seek(0)
    filename = image_file.name.rsplit('.', 1)[0] + '.jpg'
    return InMemoryUploadedFile(
        output, 'ImageField', filename,
        'image/jpeg', output.tell(), None
    )


@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display  = ('title', 'category', 'created_at', 'likes_count')
    list_filter   = ('category',)
    search_fields = ('title', 'description')

    def save_model(self, request, obj, form, change):
        # Only compress on new upload or if image was changed
        if 'image' in form.changed_data and obj.image:
            obj.image = compress_image(obj.image)
        super().save_model(request, obj, form, change)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):

    def save_model(self, request, obj, form, change):
        if 'image' in form.changed_data and obj.image:
            obj.image = compress_image(obj.image)
        super().save_model(request, obj, form, change)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display  = ('id', 'name')
    search_fields = ('name',)


@admin.register(PhotoLike)
class PhotoLikeAdmin(admin.ModelAdmin):
    list_display  = ('user', 'photo', 'liked_date')
    list_filter   = ('liked_date',)


@admin.register(Register)
class RegisterAdmin(admin.ModelAdmin):
    list_display = ('username', 'email')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'avatar_letters', 'created_at')