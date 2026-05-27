from django.contrib import admin
from django import forms
from .models import Register, Photo, Category, Gallery, PhotoLike


# ─── Multi-file upload for Gallery ───────────────────────────────────────────

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super(forms.FileInput, self).__init__(attrs=default_attrs)


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault('widget', MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, list):
            return [single_file_clean(d, initial) for d in data if d]
        return []


class GalleryAdminForm(forms.ModelForm):
    images = MultipleFileField(label='Images', required=False)

    class Meta:
        model = Gallery
        fields = []


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ['id', 'image']
    form = GalleryAdminForm

    def save_model(self, request, obj, form, change):
        files = form.cleaned_data.get('images', [])
        if files:
            for f in files:
                Gallery.objects.create(image=f)
        else:
            super().save_model(request, obj, form, change)


# ─── PhotoLike inline ─────────────────────────────────────────────────────────

class PhotoLikeInline(admin.TabularInline):
    model = PhotoLike
    extra = 0
    readonly_fields = ('user', 'liked_date')
    can_delete = False


# ─── Photo (with likes count + inline) ───────────────────────────────────────

@admin.register(Photo)
class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'image', 'get_likes_count', 'created_at')
    inlines = [PhotoLikeInline]

    def get_likes_count(self, obj):
        return obj.photo_likes.count()
    get_likes_count.short_description = 'Total Likes'


# ─── PhotoLike list ───────────────────────────────────────────────────────────

@admin.register(PhotoLike)
class PhotoLikeAdmin(admin.ModelAdmin):
    list_display = ('id', 'photo', 'get_user_id', 'get_username', 'liked_date')
    list_filter = ('photo', 'liked_date')
    search_fields = ('user__username', 'photo__id')
    readonly_fields = ('user', 'photo', 'liked_date')

    def get_user_id(self, obj):
        return obj.user_id
    get_user_id.short_description = 'User ID'

    def get_username(self, obj):
        return obj.user.username
    get_username.short_description = 'Username'


# ─── Simple registrations ─────────────────────────────────────────────────────

admin.site.register(Register)
admin.site.register(Category)


from django.contrib import admin
from .models import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):

    list_display = [
        'id',
        'user',
        'avatar_letters',
        'created_at'
    ]

    search_fields = [
        'user__username',
        'user__email'
    ]

    list_filter = [
        'created_at'
    ]

    ordering = ['-created_at']

    readonly_fields = [
        'avatar_letters',
        'created_at'
    ]