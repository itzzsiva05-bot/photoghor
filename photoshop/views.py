from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages

from .models import (
    Photo,
    Category,
    Gallery,
    PhotoLike
)

import zipfile
import os


# ======================================================
# INDEX / LOGIN
# ======================================================

def index(request):

    error = ""

    if request.method == "POST":

        # GET NEXT URL FROM HIDDEN INPUT
        next_url = request.POST.get("next")

        email = request.POST.get("email")
        password = request.POST.get("password")

        user_obj = User.objects.filter(email=email).first()

        if user_obj:

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is not None:

                auth_login(request, user)

                # PREVIOUS PAGE REDIRECT
                if next_url:
                    return redirect(next_url)

                # DEFAULT PAGE
                messages.success(request, "Account Login Successfully!")
                return redirect('live_preview')

        error = "Invalid Email or Password"

    return render(request, 'index.html', {
        'error': error
    })


# ======================================================
# LIVE PREVIEW
# ======================================================

@login_required(login_url='index')
def live_preview(request):

    return render(request, 'account/live_preview.html')


# ======================================================
# REGISTER
# ======================================================

def register(request):

    error = ""

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Check username already exists
        if User.objects.filter(username=username).exists():

            error = "Username already exists"

            return render(request, 'account/register.html', {
                'error': error
            })

        # Check email already exists
        if User.objects.filter(email=email).exists():

            error = "Email already exists"

            return render(request, 'account/register.html', {
                'error': error
            })

        # Create user
        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('index')

    return render(request, 'account/register.html', {
        'error': error
    })


# ======================================================
# HOME
# ======================================================

def home(request):

    category = request.GET.get('category')

    categories = Category.objects.all()

    if category is None:

        photos = Photo.objects.all()

    else:

        photos = Photo.objects.filter(
            category__name=category
        )

    context = {
        'categories': categories,
        'photos': photos,
    }

    return render(request, 'account/home.html', context)


# ======================================================
# PHOTO DETAIL
# ======================================================

def photo_detail(request, id):

    photo = get_object_or_404(Photo, id=id)

    return render(request, 'account/photo_detail.html', {
        'photo': photo
    })


# ======================================================
# LOGOUT
# ======================================================

def logout_view(request):

    logout(request )

    return redirect('index')


# ======================================================
# GALLERY
# ======================================================

@login_required(login_url='index')
def gallery(request):

    photos = Gallery.objects.exclude(
        image=''
    ).exclude(
        image=None
    )

    return render(request, "account/gallery.html", {
        'photos': photos
    })


# ======================================================
# DOWNLOAD ALL IMAGES
# ======================================================

@login_required(login_url='index')
def download_all_images(request):

    images = Gallery.objects.all()

    response = HttpResponse(
        content_type='application/zip'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="gallery_images.zip"'

    zip_file = zipfile.ZipFile(response, 'w')

    for img in images:

        # Check image exists
        if img.image:

            file_path = img.image.path

            # Check file exists
            if os.path.exists(file_path):

                zip_file.write(
                    file_path,
                    os.path.basename(file_path)
                )

    zip_file.close()

    return response


# ======================================================
# LIKE PHOTO
# ======================================================

@login_required(login_url='index')
@require_POST
def like_photo(request, photo_id):

    photo = get_object_or_404(
        Photo,
        pk=photo_id
    )

    today = timezone.localdate()

    existing = PhotoLike.objects.filter(
        user=request.user,
        photo=photo,
        liked_date=today
    ).first()

    # Toggle Like / Unlike
    if existing:

        existing.delete()
        liked = False

    else:

        PhotoLike.objects.create(
            user=request.user,
            photo=photo,
            liked_date=today
        )

        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': photo.likes_count
    })