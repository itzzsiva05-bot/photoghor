import os
import zipfile

import requests as req
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.decorators.http import require_POST

from .models import Category, Contact, Gallery, Photo, PhotoLike
from .models import Category as DB_Category, Photo as DB_Photo, Gallery as DB_Gallery
from .models import Gallery as GalleryModel


# ---------------------------------------------------------------------------
# Authentication
# ---------------------------------------------------------------------------

def index(request):
    """
    Login page — kept active so {% url 'index' %} and
    @login_required(login_url='index') both resolve correctly.
    Already-authenticated users are sent straight to live_preview.
    """
    if request.user.is_authenticated:
        return redirect('live_preview')

    error    = ""
    next_url = request.GET.get('next', '')

    if request.method == "POST":
        next_url = request.POST.get('next', '')
        email    = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if email and password:
            from django.contrib.auth.models import User
            user_obj = User.objects.filter(email=email).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    auth_login(request, user)
                    return redirect(next_url if next_url else 'live_preview')

        error = "Invalid Email or Password"

    return render(request, 'photoshop/index.html', {'error': error, 'next': next_url})


def custom_logout(request):
    logout(request)
    return redirect('live_preview')


# ---------------------------------------------------------------------------
# Public views
# ---------------------------------------------------------------------------

def live_preview(request):
    photos     = Photo.objects.all().order_by('-id')[:12]
    categories = Category.objects.all()
    return render(request, 'photoshop/live_preview.html', {
        'photos':     photos,
        'categories': categories,
    })


def home(request):
    col               = request.GET.get('col', '4')
    selected_category = request.GET.get('category')
    categories_list   = DB_Category.objects.all()

    if selected_category:
        photo_query = list(
            DB_Photo.objects.filter(category__name=selected_category)
                            .exclude(image='').exclude(image=None)
        )
        gallery_query = list(
            DB_Gallery.objects.filter(category__name=selected_category)
                              .exclude(image='').exclude(image=None)
        )
    else:
        photo_query   = list(DB_Photo.objects.exclude(image='').exclude(image=None))
        gallery_query = list(DB_Gallery.objects.exclude(image='').exclude(image=None))

    all_combined_photos = (
        [{'type': 'photo',   'obj': p} for p in photo_query] +
        [{'type': 'gallery', 'obj': g} for g in gallery_query]
    )

    return render(request, 'photoshop/home.html', {
        'categories': categories_list,
        'photos':     all_combined_photos,
        'col':        col,
    })


def photo_detail(request, id):
    photo = get_object_or_404(Photo, id=id)
    return render(request, 'photoshop/photo_detail.html', {'photo': photo})


def profile(request):
    return render(request, "photoshop/profile.html")


# ---------------------------------------------------------------------------
# Like (login required — redirects to login page)
# ---------------------------------------------------------------------------

@login_required(login_url='index')
@require_POST
def like_photo(request, photo_id):
    """
    Toggle a daily like for the authenticated user.
    Uses get_or_create to eliminate the race condition in the
    previous check-then-create pattern.
    """
    photo = get_object_or_404(Photo, pk=photo_id)
    today = timezone.localdate()

    like, created = PhotoLike.objects.get_or_create(
        user=request.user, photo=photo, liked_date=today
    )
    if not created:
        like.delete()

    return JsonResponse({'liked': created, 'likes_count': photo.likes_count})


# ---------------------------------------------------------------------------
# Contact
# ---------------------------------------------------------------------------

def contact(request):
    if request.method == "POST":
        Contact.objects.create(
            name    = request.POST.get('name'),
            email   = request.POST.get('email'),
            subject = request.POST.get('subject'),
            message = request.POST.get('message'),
        )
        # Return JSON if AJAX request, else redirect
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({'status': 'ok'})
        messages.success(request, "Message sent successfully!")
        return redirect('contact')
    return render(request, 'photoshop/contact.html')

