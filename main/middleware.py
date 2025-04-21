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
                'admin_dashboard', 'create', 'index'
            ]
            
            # If the path is secure and the user is not authenticated, redirect to login
            if current_url in secure_paths and not request.user.is_authenticated:
                logger.error(f"User not authenticated, redirecting to login")
                messages.warning(request, "Please log in to access this page.")
                return redirect('login')
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