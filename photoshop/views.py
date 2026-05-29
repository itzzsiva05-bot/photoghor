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


# ─────────────────────────────────────────
# INDEX / LOGIN VIEW
# ─────────────────────────────────────────
def index(request):
    """
    Login page. On success → redirect to live_preview.
    Already logged-in users are sent straight there.
    """
    if request.user.is_authenticated:
        return redirect('live_preview')

    error = ""
    next_url = request.GET.get('next', '')

    if request.method == "POST":
        next_url = request.POST.get('next', '')
        email    = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        if email and password:
            user_obj = User.objects.filter(email=email).first()
            if user_obj:
                user = authenticate(request, username=user_obj.username, password=password)
                if user:
                    auth_login(request, user)
                    return redirect(next_url if next_url else 'live_preview')

        error = "Invalid Email or Password"

    return render(request, 'photoshop/index.html', {
        'error': error,
        'next': next_url,
    })


# ─────────────────────────────────────────
# LIVE PREVIEW VIEW
# ─────────────────────────────────────────

def live_preview(request):
    """
    Main preview page — only logged-in users can access.
    """
    photos     = Photo.objects.all().order_by('-id')[:12]
    categories = Category.objects.all()
    return render(request, 'photoshop/live_preview.html', {
        'photos': photos,
        'categories': categories,
    })


# ─────────────────────────────────────────
# LOGOUT VIEW
# ─────────────────────────────────────────

def custom_logout(request):
    logout(request)
    return redirect('live_preview')


# ─────────────────────────────────────────
# REGISTER VIEW
# ─────────────────────────────────────────
def register(request):
    """
    User registration. Validates username & email uniqueness.
    On success → redirect to index (login page).
    """
    if request.user.is_authenticated:
        return redirect('live_preview')

    if request.method != "POST":
        return render(request, 'account/register.html', {'error': ''})

    username = request.POST.get("username", "").strip()
    email    = request.POST.get("email", "").strip()
    password = request.POST.get("password", "")

    if not username or not email or not password:
        return render(request, 'account/register.html', {'error': 'All fields are required'})

    if User.objects.filter(username=username).exists():
        return render(request, 'account/register.html', {'error': 'Username already exists'})

    if User.objects.filter(email=email).exists():
        return render(request, 'account/register.html', {'error': 'Email already exists'})

    User.objects.create_user(username=username, email=email, password=password)
    messages.success(request, "Account created! Please log in.")
    return redirect('index')


# ─────────────────────────────────────────
# HOME VIEW
# ─────────────────────────────────────────
def home(request):
    """
    Public home page. Supports filtering by category.
    """
    category   = request.GET.get('category')
    categories = Category.objects.all()

    if category:
        photos = Photo.objects.filter(category__name=category)
    else:
        photos = Photo.objects.all()

    return render(request, 'photoshop/home.html', {
        'categories': categories,
        'photos': photos,
    })


# ─────────────────────────────────────────
# PHOTO DETAIL VIEW
# ─────────────────────────────────────────
def photo_detail(request, id):
    """
    Single photo detail page.
    """
    photo = get_object_or_404(Photo, id=id)
    return render(request, 'photoshop/photo_detail.html', {'photo': photo})


# ─────────────────────────────────────────
# GALLERY VIEW
# ─────────────────────────────────────────
@login_required(login_url='index')
def gallery(request):
    """
    Gallery page — shows all gallery images (login required).
    """
    photos = Gallery.objects.exclude(image='').exclude(image=None)
    return render(request, "photoshop/gallery.html", {'photos': photos})


# ─────────────────────────────────────────
# DOWNLOAD ALL IMAGES (ZIP)
# ─────────────────────────────────────────
@login_required(login_url='index')
def download_all_images(request):
    import requests as req
    images   = Gallery.objects.all()
    response = HttpResponse(content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="gallery_images.zip"'

    with zipfile.ZipFile(response, 'w') as zf:
        for img in images:
            if img.image:
                url = img.image.url          # ✅ Cloudinary URL
                r = req.get(url)
                if r.status_code == 200:
                    zf.writestr(os.path.basename(img.image.name), r.content)

    return response

# ─────────────────────────────────────────
# LIKE / UNLIKE PHOTO (AJAX)
# ─────────────────────────────────────────
@login_required(login_url='index')
@require_POST
def like_photo(request, photo_id):
    """
    Toggle like/unlike on a photo (one like per user per day).
    Returns JSON: { liked: bool, likes_count: int }
    """
    photo    = get_object_or_404(Photo, pk=photo_id)
    today    = timezone.localdate()
    existing = PhotoLike.objects.filter(
        user=request.user,
        photo=photo,
        liked_date=today
    ).first()

    if existing:
        existing.delete()
        liked = False
    else:
        PhotoLike.objects.create(user=request.user, photo=photo, liked_date=today)
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes_count': photo.likes_count,
    })