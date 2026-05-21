from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Category 
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Gallery
from django.contrib.auth.decorators import login_required





# ================= INDEX / LOGIN =================
def index(request):

    error = ""

    # URL-la irundhu next value edukkum
    next_url = request.GET.get('next')

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        # EMAIL -> USERNAME FETCH
        user_obj = User.objects.filter(email=email).first()

        if user_obj:

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user is not None:

                login(request, user)

                # login success na previous requested page open
                if next_url:
                    return redirect(next_url)

                return redirect('live_preview')

        error = "Invalid Email or Password"

    return render(request, 'index.html', {
        'error': error
    })


# ================= REGISTER =================

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        # CREATE DJANGO USER

        User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        return redirect('index')

    return render(request, 'register.html')


# ================= HOME =================

def home(request):

    category = request.GET.get('category')

    categories = Category.objects.all()

    if category == None:

        photos = Photo.objects.all()

    else:

        photos = Photo.objects.filter(
            category__name=category
        )

    context = {
        'categories': categories,
        'photos': photos,
    }

    return render(request, 'home.html', context)


# ================= PHOTO DETAIL =================

def photo_detail(request, id):

    photo = get_object_or_404(Photo, id=id)

    return render(request, 'photo_detail.html', {
        'photo': photo
    })


# ================= LIVE PREVIEW =================

def live_preview(request):

    return render(request, 'live_preview.html')


# ================= LOGOUT =================
def logout_view(request):

    request.session.flush()

    return redirect('live_preview')



@login_required(login_url='index')
def gallery(request):
    photos = Gallery.objects.exclude(image='').exclude(image=None)
    return render(request, "gallery.html", {
        'photos': photos
    })

import zipfile
import os

from django.http import HttpResponse
from .models import Gallery


def download_all_images(request):

    images = Gallery.objects.all()

    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="gallery_images.zip"'

    zip_file = zipfile.ZipFile(response, 'w')

    for img in images:

        # CHECK image exists
        if img.image:

            file_path = img.image.path

            # CHECK file exists in media folder
            if os.path.exists(file_path):

                zip_file.write(
                    file_path,
                    os.path.basename(file_path)
                )

    zip_file.close()

    return response

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Photo, PhotoLike

@login_required
@require_POST
def like_photo(request, photo_id):
    photo = Photo.objects.get(pk=photo_id)
    today = timezone.localdate()   # current date only

    existing = PhotoLike.objects.filter(
        user=request.user,
        photo=photo,
        liked_date=today
    ).first()

    if existing:
        # Already liked today — unlike (toggle)
        existing.delete()
        liked = False
    else:
        # First like today — create
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