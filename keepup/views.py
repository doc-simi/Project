from django.core.exceptions import ValidationError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError

from django.utils.timezone import localtime, now, get_current_timezone

from .models import Profile_pic, User
from .validate import validate_image_size
# Create your views here.


@login_required
def home(request):
    return render(request, "keepup/index.html")

def register(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == "POST":
        
        firstname = request.POST["firstname"].capitalize()
        lastname = request.POST["lastname"].capitalize()
        email = request.POST["email"]
        date = request.POST["DOB"]
        sex = request.POST["sex"]
        profile_pic = request.FILES["profile_pic"]
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["repeatpassword"]
        if password != confirmation:
            return render(request, "keepup/register.html", {
                "message": "Passwords must match."
            })

        try:
            validate_image_size(profile_pic)
        except ValidationError as e:
            return render(request, "keepup/register.html", {
                "message": e
            })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password, firstname, lastname, sex, date)
            Profile_pic.objects.add_profile_pic(user.id, profile_pic)
            login(request, user)
        except IntegrityError:
            return render(request, "keepup/register.html", {
                "message": "Username already taken."
            })
        
        return HttpResponseRedirect(reverse("home"))

    return render(request, "keepup/register.html")


def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('home'))

    if request.method == "POST":
        next = request.POST["next"]
        
        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            print(next)
            if next is not None:
                return HttpResponseRedirect(reverse("home"))
            else:
                return redirect(next)
        else:
            return render(request, "keepup/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "keepup/login.html")


def logout_view(request):
    logout(request)
    return redirect(reverse("homepage"))

def forgot_password(request):
    pass
    
def newTask(request):
    return render(request, "keepup/create/task.html")

def newTodo(request):
    return render(request, "keepup/create/todo.html")

def newReminder(request):
    return render(request, "keepup/create/reminder.html")

def viewTask(request):
    return render(request, "keepup/data/task.html")

def viewTodo(request):
    return render(request, "keepup/data/todo.html")

def viewReminder(request):
    return render(request, "keepup/data/reminder.html")

def messages(request):
    return render(request, "keepup/user/messages.html")

def notification(request):
    return render(request, "keepup/user/notification.html")

def profile(request):
    return render(request, "keepup/user/profile.html")

def settings(request):
    return render(request, "keepup/user/settings.html")

def about(request):
    return render(request, "keepup/tools/about.html")

def contact(request):
    return render(request, "keepup/tools/contact.html")

def update(request):
    return render(request, "keepup/tools/update.html")

