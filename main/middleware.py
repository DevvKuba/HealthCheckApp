from django.shortcuts import redirect
from django.urls import resolve
from django.contrib import messages
import logging

# Set up logging
logger = logging.getLogger(__name__)

class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Code to be executed for each request before the view is called
        
        try:
            # Get current URL name
            current_url = resolve(request.path_info).url_name
            logger.error(f"Request path: {request.path_info}, URL name: {current_url}")
            
            # List of secure paths that require authentication
            secure_paths = [
                'dashboard', 'chat', 'settings', 'project_health', 
                'admin_dashboard', 'admin_projects', 'create', 'index'
            ]
            
            # Paths that don't require approval check
            approval_exempt_paths = ['waiting_approval', 'logout', 'login']
            
            # If the path is secure and the user is not authenticated, redirect to login
            if current_url in secure_paths and not request.user.is_authenticated:
                logger.error(f"User not authenticated, redirecting to login")
                messages.warning(request, "Please log in to access this page.")
                return redirect('login')
            
            # If user is authenticated, check role for appropriate access
            if request.user.is_authenticated:
                try:
                    from register.models import UserProfile
                    profile = UserProfile.objects.get(user=request.user)
                    
                    # Check if employee is approved (admins are always approved)
                    if (profile.role in ['employee', 'manager'] and not profile.is_approved 
                            and current_url not in approval_exempt_paths):
                        messages.info(request, "Your account is pending approval from your company admin.")
                        return redirect('waiting_approval')
                    
                    # Admin-only paths
                    admin_paths = ['admin_dashboard', 'admin_projects']
                    
                    # Employee/non-admin paths
                    employee_paths = ['dashboard']
                    
                    # Redirect admins trying to access employee pages
                    if current_url in employee_paths and profile.role == 'admin':
                        messages.info(request, "Redirected to admin dashboard.")
                        return redirect('admin_dashboard')
                    
                    # Redirect non-admins trying to access admin pages
                    if current_url in admin_paths and profile.role != 'admin':
                        messages.info(request, "Redirected to employee dashboard.")
                        return redirect('dashboard')
                        
                except Exception as e:
                    # If there's an error checking the profile, log it but don't block
                    logger.error(f"Error checking user profile: {str(e)}")
            
        except Exception as e:
            # If URL resolution fails, log the error but don't block the request
            logger.error(f"Error in SecurityMiddleware: {str(e)}")
            
        response = self.get_response(request)
        
        # Add security headers to the response
        response['X-Content-Type-Options'] = 'nosniff'
        response['X-Frame-Options'] = 'DENY'
        response['X-XSS-Protection'] = '1; mode=block'
        response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response 