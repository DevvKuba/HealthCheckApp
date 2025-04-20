from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/home")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})

# Add new view functions for login and signup pages
def login_view(request):
    return render(request, "register/login.html")

def signup_view(request):
    return render(request, "register/signup.html")

# Add logout view
def logout_view(request):
    logout(request)
    return redirect('login')
