from django.shortcuts import render, redirect, get_object_or_404
from .models import Photo, Category
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout



# ================= INDEX / LOGIN =================

def index(request):

    error = ""

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