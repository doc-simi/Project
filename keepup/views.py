import os
from django.core.exceptions import ValidationError
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password, check_password
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
        try:
            sex = request.POST["sex"]
            profile_pic = request.FILES["profile_pic"]
        except MultiValueDictKeyError:
            profile_pic = None
            sex = 'Undisclosed'
        
        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["repeatpassword"]
        if password != confirmation:
            return render(request, "keepup/register.html", {
                "message": "Passwords must match."
            })

        if profile_pic:
            try:
                validate_image_size(profile_pic)
            except ValidationError as e:
                return render(request, "keepup/register.html", {
                    "message": e
                })
        
        # Attempt to create new user
        try:
            user = User.objects.create_user(email, password, firstname, lastname, sex, date)
            profile = Profile_pic.objects.add_profile_pic(user.id, profile_pic)
            if profile_pic == None:
                profile.profile_pic = 'profile_image\profile.jpg'
                profile.save()
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
            if not next:
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
    
@login_required
def newTask(request):
    return render(request, "keepup/create/task.html")

@login_required
def newTodo(request):
    return render(request, "keepup/create/todo.html")

@login_required
def newReminder(request):
    return render(request, "keepup/create/reminder.html")

@login_required
def viewTask(request):
    return render(request, "keepup/data/task.html")

@login_required
def viewTodo(request):
    return render(request, "keepup/data/todo.html")

@login_required
def viewReminder(request):
    return render(request, "keepup/data/reminder.html")

@login_required
def messages(request):
    return render(request, "keepup/user/messages.html")

@login_required
def notification(request):
    return render(request, "keepup/user/notification.html")

@login_required
def profile(request):
    """
    Provide the user with all information about his/her account
    Fortunately we can get thtese details from the request tag in our templates
    """
    return render(request, "keepup/user/profile.html")

@login_required
def settings(request):
    if request.method == "POST":
        selected = request.POST.getlist('check-edits')
        
        # Create a list of conditional statements for every 
        # possible variables in the selected list
        user = User.objects.get(pk=request.user.id)

        if 'password' in selected:
            new_password = request.POST["password"]
            reapeat_new_password = request.POST["repeatpassword"]
            old_password = request.POST["oldpassword"]

            if new_password != reapeat_new_password:
                return render(request, 'keepup/user/settings.html', {
                    "message": "New Password doesn't match"
                })

            if not check_password(old_password, request.user.password):
                return render(request, 'keepup/user/settings.html', {
                    "message": "Old Password is not correct"
                })
            
            password = make_password(new_password)
            user.password = password
            

        if 'firstname' in selected:
            user.first_name = request.POST["firstname"]
        
        if 'lastname' in selected:
            user.last_name = request.POST["lastname"]
            user.save()
        
        if 'email' in selected:
            if request.POST["email"] != request.user.email:
                try:
                    user.email = request.POST["email"]
                    user.save()
                except IntegrityError:
                    return render(request, "keepup/user/settings.html", {
                        "message": "Username already taken."
                    })
            

        if 'DOB' in selected:
            user.D_O_B = request.POST["DOB"]

        if 'sex' in selected:
            user.sex = request.POST["sex"]

        if 'profile_pic' in selected:
            try:
                profile_pic = request.FILES["profile_pic"]
            except MultiValueDictKeyError:
                profile_pic = None
            if profile_pic:
                try:
                    # Validate image
                    validate_image_size(profile_pic)
                    profile = Profile_pic.objects.get(user_id=request.user.id)
                    
                    # Get the path of the image so it can be deleted
                    old_pic = "keepup" + profile.profile_pic.url
                    if os.path.exists(old_pic):
                        os.remove(old_pic)
                    
                    # Clear the name in the DB. This will make sure rewriting of file will cause no filename repitition 
                    profile.profile_pic = ""
                    profile.save()

                    # Then you can save the new file
                    profile.profile_pic = profile_pic
                    profile.save()
                except ValidationError as e:
                    return render(request, "keepup/user/settings.html", {
                        "message": e
                    })
                

        user.save()
        return redirect(reverse('profile'))
    else:
        return render(request, "keepup/user/settings.html")

@login_required
def about(request):
    return render(request, "keepup/tools/about.html")

@login_required
def contact(request):
    return render(request, "keepup/tools/contact.html")

@login_required
def update(request):
    return render(request, "keepup/tools/update.html")

