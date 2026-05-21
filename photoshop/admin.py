from django.contrib import admin
from django import forms
from .models import Register, Photo, Category, Gallery


class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True  # Django internal check bypass

    def __init__(self, attrs=None):
        default_attrs = {'multiple': 'multiple'}
        if attrs:
            default_attrs.update(attrs)
        super(forms.FileInput, self).__init__(attrs=default_attrs)  # Widget.__init__ direct call


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


admin.site.register(Register)
admin.site.register(Photo)
admin.site.register(Category)