from django.shortcuts import render, redirect, get_object_or_404
from .forms import RegisterForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import Company, UserProfile

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
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            
            if user is not None:
                login(request, user)
                messages.success(request, f"Welcome back, {username}!")
                
                # Redirect based on user role
                try:
                    profile = UserProfile.objects.get(user=user)
                    if profile.role == 'admin':
                        return redirect('admin_dashboard')
                    else:
                        return redirect('dashboard')
                except UserProfile.DoesNotExist:
                    messages.warning(request, "Profile not found. Using default dashboard.")
                    return redirect('dashboard')
                except Exception as e:
                    messages.warning(request, f"Error determining role. Using default dashboard.")
                    return redirect('dashboard')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid login details.")
    
    form = AuthenticationForm()
    return render(request, "register/login.html", {"form": form})

def signup_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            
            # If they're an admin who created a company, redirect to company code page
            try:
                profile = UserProfile.objects.get(user=user)
                if profile.role == 'admin' and profile.company:
                    return redirect(reverse('company_code'))
            except UserProfile.DoesNotExist:
                pass
                
            return redirect(reverse('dashboard'))
        else:
            messages.error(request, "Unsuccessful registration. Invalid information.")
            print(form.errors)  # Log form errors for debugging
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

@login_required
def company_code_view(request):
    """View for admins to see their company access code"""
    try:
        # Check if user is admin
        profile = UserProfile.objects.get(user=request.user)
        if profile.role != 'admin':
            messages.warning(request, "Only admins can view company codes")
            return redirect('dashboard')
            
        # If admin, proceed with the view
        companies = Company.objects.filter(created_by=request.user)
        return render(request, "register/company_code.html", {"companies": companies})
    
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found")
        return redirect('dashboard')
    except Exception as e:
        messages.error(request, f"Error: {str(e)}")
        return redirect('dashboard')

# Add waiting approval view
@login_required
def waiting_approval(request):
    """View for employees to see when waiting for admin approval"""
    try:
        profile = UserProfile.objects.get(user=request.user)
        if profile.is_approved:
            # If already approved, redirect to appropriate dashboard
            if profile.role == 'admin':
                return redirect('admin_dashboard')
            else:
                return redirect('dashboard')
                
        # Get company info if available
        company = profile.company
        
        return render(request, "register/waiting_approval.html", {
            "username": request.user.username,
            "company": company,
            "profile": profile
        })
    
    except UserProfile.DoesNotExist:
        messages.error(request, "Profile not found")
        return redirect('logout')
