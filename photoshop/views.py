from django.shortcuts import render ,redirect ,get_object_or_404
from .models import Register
from .models import Photo , Category
user_data={}


def index(request):

    error = ""

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        # EMAIL CHECK

        email_check = Register.objects.filter(
            email=email
        ).first()

        if not email_check:

            error = "Email ID Incorrect"

        else:

            # PASSWORD CHECK

            password_check = Register.objects.filter(
                email=email,
                password=password
            ).first()

            if not password_check:

                error = "Password Incorrect"

            else:

                return redirect('live_preview')

    return render(request, 'index.html', {

        'error': error

    })


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

def register(request):

    if request.method == "POST":

        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        Register.objects.create(
            username=username,
            email=email,
            password=password
        )

        return redirect('index')

    return render(request, 'register.html')

def photo_detail(request, id):

    photo = get_object_or_404(Photo, id=id)

    return render(request, 'photo_detail.html', {
        'photo': photo
    })



def live_preview(request):

    return render(request, 'live_preview.html')