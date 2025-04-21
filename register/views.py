from django.shortcuts import render, redirect
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse

# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(reverse('dashboard'))
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()

    return render(request, "register/register.html", {"form": form})

# Enhanced login view with authentication
def login_view(request):
    print(f"Login view called with method: {request.method}")
    if request.method == "POST":
        print("Processing POST request for login")
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            print("Form is valid")
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            print(f"Authentication result: {'Success' if user else 'Failed'}")
            if user is not None:
                login(request, user)
                print(f"User {username} logged in successfully")
                messages.info(request, f"You are now logged in as {username}.")
                # Use reverse to get the dashboard URL
                dashboard_url = reverse('dashboard')
                print(f"Redirecting to: {dashboard_url}")
                return redirect(dashboard_url)
            else:
                messages.error(request, "Invalid username or password.")
        else:
            print(f"Form errors: {form.errors}")
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "register/login.html", {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect(reverse('dashboard'))
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = RegisterForm()
    return render(request, "register/signup.html", {"form": form})

# Add logout view
def logout_view(request):
    print("Logging out user:", request.user.username if request.user.is_authenticated else "Not authenticated")
    logout(request)
    # Clear any session data
    request.session.flush()
    messages.info(request, "You have successfully logged out.") 
    return redirect(reverse('login'))
