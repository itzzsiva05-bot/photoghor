from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.utils import timezone
from django.contrib import messages
from .models import Photo, Category, Gallery, PhotoLike
import zipfile, os



from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def index(request):

    error = ""

    next_url = request.GET.get('next')

    if request.method == "POST":

        next_url = request.POST.get('next')

        email = request.POST.get("email")

        password = request.POST.get("password")

        user_obj = User.objects.filter(email=email).first()

        if user_obj:

            user = authenticate(
                request,
                username=user_obj.username,
                password=password
            )

            if user:

                auth_login(request, user)

                return redirect('live_preview')

        error = "Invalid Email or Password"

    return render(request, 'photoshop/index.html', {
        'error': error,
        'next': next_url
    })


def live_preview(request):

    return render(request, 'photoshop/live_preview.html')


def custom_logout(request):

    logout(request)

    return redirect('live_preview')

def register(request):
    if request.method != "POST":
        return render(request, 'account/register.html', {'error': ''})
    username = request.POST.get("username")
    email    = request.POST.get("email")
    password = request.POST.get("password")
    if User.objects.filter(username=username).exists():
        return render(request, 'account/register.html', {'error': 'Username already exists'})
    if User.objects.filter(email=email).exists():
        return render(request, 'account/register.html', {'error': 'Email already exists'})
    User.objects.create_user(username=username, email=email, password=password)
    return redirect('index')


def home(request):
    category   = request.GET.get('category')
    categories = Category.objects.all()
    photos     = Photo.objects.filter(category__name=category) if category else Photo.objects.all()
    return render(request, 'photoshop/home.html', {'categories': categories, 'photos': photos})


def photo_detail(request, id):
    photo = get_object_or_404(Photo, id=id)
    return render(request, 'photoshop/photo_detail.html', {'photo': photo})





@login_required
def gallery(request):
    photos = Gallery.objects.exclude(image='').exclude(image=None)
    return render(request, "photoshop/gallery.html", {'photos': photos})


@login_required
def download_all_images(request):
    images   = Gallery.objects.all()
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="gallery_images.zip"'
    with zipfile.ZipFile(response, 'w') as zf:
        for img in images:
            if img.image and os.path.exists(img.image.path):
                zf.write(img.image.path, os.path.basename(img.image.path))
    return response


@login_required
@require_POST
def like_photo(request, photo_id):
    photo    = get_object_or_404(Photo, pk=photo_id)
    today    = timezone.localdate()
    existing = PhotoLike.objects.filter(user=request.user, photo=photo, liked_date=today).first()
    if existing:
        existing.delete()
        liked = False
    else:
        PhotoLike.objects.create(user=request.user, photo=photo, liked_date=today)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': photo.likes_count})