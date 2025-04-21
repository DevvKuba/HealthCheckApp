from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from .models import ToDoList, Item, Project, Team, Department, ProjectImprovement
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count
from django.contrib.auth.models import User
from django.utils.dateparse import parse_date

# Create your views here.
def index(response, id):
    ls = ToDoList.objects.get(id=id)
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                if response.POST.get("c" + str(item.id)) == "clicked":
                    item.complete = True
                else:
                    item.complete = False
                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")

            if len(txt) > 2:
                ls.item_set.create(text=txt, complete=False)
            else:
                print("invalid")


    return render(response, "main/list.html", {"ls": ls})

def home(response):
    return render(response, "main/home.html", {})

@login_required
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)

        if form.is_valid():
            n = form.cleaned_data["name"]
            t = ToDoList(name=n)
            t.save()
        return HttpResponseRedirect("/%i" %t.id)
    else:
        form = CreateNewList()
    return render(response, "main/create.html", {"form": form})

# Add dashboard view - protected route
@login_required
def dashboard(request):
    print("Dashboard view is being called!")
    
    # Get projects data
    projects = Project.objects.all().order_by('-created_at')
    
    # Get stats
    total_projects = Project.objects.count()
    active_projects = Project.objects.filter(status='active').count()
    completed_projects = Project.objects.filter(status='completed').count()
    team_members = User.objects.count()
    
    # Get teams and departments for dropdown
    teams = Team.objects.all()
    departments = Department.objects.all()
    
    # Check if we need to create default data
    if teams.count() == 0:
        # Create a default department
        default_dept = Department.objects.create(name="General", code="GEN")
        # Create a default team
        Team.objects.create(name="Default Team", code="DEF", department=default_dept)
        # Refresh data
        teams = Team.objects.all()
        departments = Department.objects.all()
    
    # Get current user's username to display in the dashboard
    context = {
        'username': request.user.username,
        'user': request.user,
        'projects': projects,
        'teams': teams,
        'departments': departments,
        'total_projects': total_projects,
        'active_projects': active_projects,
        'completed_projects': completed_projects,
        'team_members': team_members
    }
    return render(request, "main/dashboard.html", context)

# View to handle adding a new project
@login_required
def add_project(request):
    if request.method == "POST":
        # Get form data
        name = request.POST.get('name')
        description = request.POST.get('description', '')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date', None)
        status = request.POST.get('status')
        health = request.POST.get('health')
        team_id = request.POST.get('team')
        department_id = request.POST.get('department')
        
        try:
            # Get related objects
            team = Team.objects.get(id=team_id)
            department = Department.objects.get(id=department_id)
            
            # Create the project
            project = Project(
                name=name,
                description=description,
                start_date=parse_date(start_date),
                status=status,
                health=health,
                team=team,
                department=department,
                created_by=request.user
            )
            
            # Add end date if provided
            if end_date:
                project.end_date = parse_date(end_date)
                
            project.save()
            
            # Add current user as a member
            project.members.add(request.user)
            
            messages.success(request, f"Project '{name}' created successfully!")
        except Exception as e:
            messages.error(request, f"Error creating project: {str(e)}")
        
    return redirect('dashboard')

# Add chat view - protected route
@login_required
def chat(request):
    context = {
        'username': request.user.username,
        'user': request.user
    }
    return render(request, "main/chat.html", context)

# Add settings view - protected route
@login_required
def settings(request):
    user = request.user
    
    # Handle form submission
    if request.method == "POST":
        try:
            # Get form data
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            new_password = request.POST.get('new_password', '')
            
            # Update user profile
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            
            # Update password if provided and valid
            if new_password:
                user.set_password(new_password)
                # This will require the user to login again
                messages.info(request, "Password updated. Please login again.")
            
            user.save()
            
            # If the password was not changed, display success message
            if not new_password:
                messages.success(request, "Profile information updated successfully!")
            return redirect('settings')
            
        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
    
    context = {
        'username': user.username,
        'user': user,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email
    }
    return render(request, "main/settings.html", context)

# Add a save_settings view for handling form submission
@login_required
def save_settings(request):
    if request.method == "POST":
        try:
            user = request.user
            
            # Get form data
            first_name = request.POST.get('first_name', '')
            last_name = request.POST.get('last_name', '')
            email = request.POST.get('email', '')
            new_password = request.POST.get('new_password', '')
            
            # Update user profile
            user.first_name = first_name
            user.last_name = last_name
            user.email = email
            
            # Update password if provided
            if new_password:
                user.set_password(new_password)
                user.save()
                # This will log the user out
                messages.info(request, "Password updated. Please login again.")
                return redirect('login')
            
            user.save()
            messages.success(request, "Profile information updated successfully!")
            
        except Exception as e:
            messages.error(request, f"Error updating profile: {str(e)}")
    
    return redirect('settings')

# Add project health view - protected route
@login_required
def project_health(request):
    # Get all projects for the dropdown
    projects = Project.objects.all().order_by('name')
    
    # Get recent health assessments and improvement suggestions
    improvements = ProjectImprovement.objects.select_related('project', 'user').order_by('-created_at')[:10]
    
    # Check if user is admin or project manager (has created projects)
    is_manager = request.user.is_staff or Project.objects.filter(created_by=request.user).exists()
    
    context = {
        'username': request.user.username,
        'user': request.user,
        'projects': projects,
        'improvements': improvements,
        'is_manager': is_manager
    }
    return render(request, "main/project_health.html", context)

# Add save_project_health view to handle health assessment submissions
@login_required
def save_project_health(request):
    if request.method == "POST":
        try:
            # Get form data
            project_id = request.POST.get('project_id')
            health_percentage = request.POST.get('health_percentage')
            comment = request.POST.get('comment', '')
            
            # Get the project
            project = Project.objects.get(id=project_id)
            
            # Update project health based on percentage
            if int(health_percentage) >= 70:
                health_status = 'good'
            elif int(health_percentage) >= 30:
                health_status = 'needs_work'
            else:
                health_status = 'poor'
            
            # Save the health status
            project.health = health_status
            project.save()
            
            # Here you could also save the assessment history or comments
            # For example, if you had a ProjectHealthAssessment model:
            # ProjectHealthAssessment.objects.create(
            #     project=project,
            #     percentage=health_percentage,
            #     status=health_status,
            #     comment=comment,
            #     assessed_by=request.user
            # )
            
            messages.success(request, f"Health status for '{project.name}' updated successfully!")
        except Project.DoesNotExist:
            messages.error(request, "Project not found. Please select a valid project.")
        except Exception as e:
            messages.error(request, f"Error updating project health: {str(e)}")
    
    return redirect('project_health')

# Add improvement suggestion for a project - for admins and project managers
@login_required
def add_improvement(request):
    if request.method == "POST":
        try:
            # Check if user is admin or project manager
            is_manager = request.user.is_staff or Project.objects.filter(created_by=request.user).exists()
            
            if not is_manager:
                messages.error(request, "Only project managers or admins can add improvement suggestions.")
                return redirect('project_health')
            
            # Get form data
            project_id = request.POST.get('project_id')
            suggestion = request.POST.get('suggestion')
            
            if not suggestion.strip():
                messages.error(request, "Please provide an improvement suggestion.")
                return redirect('project_health')
            
            # Get the project
            project = Project.objects.get(id=project_id)
            
            # Create the improvement suggestion
            ProjectImprovement.objects.create(
                project=project,
                user=request.user,
                suggestion=suggestion
            )
            
            messages.success(request, f"Improvement suggestion for '{project.name}' added successfully!")
        except Project.DoesNotExist:
            messages.error(request, "Project not found. Please select a valid project.")
        except Exception as e:
            messages.error(request, f"Error adding improvement suggestion: {str(e)}")
    
    return redirect('project_health')

# Toggle implementation status of improvement suggestion - for admins and project managers
@login_required
def toggle_improvement(request, improvement_id):
    if request.method == "POST":
        try:
            # Check if user is admin or project manager
            is_manager = request.user.is_staff or Project.objects.filter(created_by=request.user).exists()
            
            if not is_manager:
                return JsonResponse({'success': False, 'message': "Only project managers or admins can update improvement status."})
            
            # Get the improvement
            improvement = get_object_or_404(ProjectImprovement, id=improvement_id)
            
            # Toggle implementation status
            improvement.is_implemented = not improvement.is_implemented
            improvement.save()
            
            return JsonResponse({
                'success': True, 
                'is_implemented': improvement.is_implemented
            })
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
    
    return JsonResponse({'success': False, 'message': "Invalid request method."})

# Add admin dashboard view - protected route
@login_required
def admin_dashboard(request):
    context = {
        'username': request.user.username,
        'user': request.user
    }
    return render(request, "main/admin_dashboard.html", context)



