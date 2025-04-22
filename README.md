# HealthCheckApp

A comprehensive web application for tracking project health status, team collaboration, and administrative management.

## Table of Contents

1. [Project Overview](#project-overview)
2. [Technologies Used](#technologies-used)
3. [Installation](#installation)
4. [Project Structure](#project-structure)
5. [Routes & URL Patterns](#routes--url-patterns)
6. [Features](#features)
7. [Running the Project](#running-the-project)
8. [User Guide](#user-guide)
9. [Troubleshooting](#troubleshooting)

## Project Overview

HealthCheckApp is a Django-based web application designed to help teams track and manage project health status. It provides interfaces for user registration, project health tracking, team communication, settings management, and administrative controls.

The application includes:
- User authentication (login and registration)
- Role-based access control (admin, employee, manager, client)
- Employee approval system for company administrators
- Dashboard for project metrics
- Project health status tracking
- Team chat functionality
- User settings management
- Admin dashboard for system management

## Technologies Used

- **Backend**: Django 5.2
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite (default Django database)
- **Dependencies**:
  - django-crispy-forms

## Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)

### Step-by-Step Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/HealthCheckApp.git
cd HealthCheckApp
```

2. **Create a virtual environment**

```bash
python -m venv venv
```

3. **Activate the virtual environment**

- On Windows:
```bash
venv\Scripts\activate
```

- On macOS/Linux:
```bash
source venv/bin/activate
```

4. **Install dependencies**

```bash
pip install django
pip install django-crispy-forms
```

5. **Initialize the database**

```bash
python manage.py migrate
```

6. **Create an admin user (optional)**

```bash
python manage.py createsuperuser
```

## Project Structure

The HealthCheckApp is organized into the following structure:

```
HealthCheckApp/
├── HealthCheckApp/          # Main project directory
│   ├── __init__.py
│   ├── asgi.py
│   ├── settings.py          # Project settings
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py
├── main/                    # Main application
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py             # Form definitions
│   ├── middleware.py        # Security middleware
│   ├── migrations/          # Database migrations
│   ├── models.py            # Data models
│   ├── templates/           # HTML templates
│   │   └── main/
│   │       ├── admin_dashboard.html
│   │       ├── admin_projects.html
│   │       ├── base.html
│   │       ├── chat.html
│   │       ├── create.html
│   │       ├── dashboard.html
│   │       ├── home.html
│   │       ├── list.html
│   │       ├── project_health.html
│   │       └── settings.html
│   ├── templatetags/        # Custom template tags
│   ├── tests.py
│   ├── urls.py              # App URL configuration
│   └── views.py             # View functions
├── register/                # User registration app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py             # Registration forms
│   ├── migrations/
│   ├── models.py            # User and company models
│   ├── templates/           # Registration templates
│   │   └── register/
│   │       ├── company_code.html
│   │       ├── login.html
│   │       ├── register.html
│   │       ├── signup.html
│   │       └── waiting_approval.html
│   ├── tests.py
│   └── views.py             # Registration views
├── manage.py                # Django management script
├── db.sqlite3               # SQLite database
└── README.md                # This documentation
```

## Routes & URL Patterns

The application includes the following URL routes:

### Main Project URLs (`HealthCheckApp/urls.py`)

| URL Pattern | View Function | Name | Description |
|-------------|--------------|------|-------------|
| `admin/` | Django admin site | - | Django's built-in admin interface |
| `register/` | `register.views.register` | `register` | User registration page |
| `login/` | `register.views.login_view` | `login` | User login page |
| `signup/` | `register.views.signup_view` | `signup` | User signup page |
| `logout/` | `register.views.logout_view` | `logout` | User logout handler |
| `company-code/` | `register.views.company_code_view` | `company_code` | View company access codes |
| `waiting-approval/` | `register.views.waiting_approval` | `waiting_approval` | Waiting for admin approval page |
| `''` | RedirectView to login | - | Root URL redirects to login |
| `''` | Include main.urls | - | Includes all URLs from main app |

### Main App URLs (`main/urls.py`)

| URL Pattern | View Function | Name | Description |
|-------------|--------------|------|-------------|
| `<int:id>` | `views.index` | `index` | Detail view for a specific item by ID |
| `home/` | `views.home` | `home` | Homepage |
| `create/` | `views.create` | `create` | Create new item page |
| `dashboard/` | `views.dashboard` | `dashboard` | Main dashboard |
| `chat/` | `views.chat` | `chat` | Chat interface |
| `settings/` | `views.settings` | `settings` | User settings page |
| `project-health/` | `views.project_health` | `project_health` | Project health tracking page |
| `save-project-health/` | `views.save_project_health` | `save_project_health` | Handle health status updates |
| `admin-dashboard/` | `views.admin_dashboard` | `admin_dashboard` | Admin dashboard |
| `admin-projects/` | `views.admin_projects` | `admin_projects` | Admin project management |
| `add-project/` | `views.add_project` | `add_project` | Create new project handler |
| `approve-employee/<int:user_id>/` | `views.approve_employee` | `approve_employee` | Approve employee access |
| `reject-employee/<int:user_id>/` | `views.reject_employee` | `reject_employee` | Reject employee access |

## Features

### Authentication System

- **Login**: Email and password-based authentication
- **Sign Up**: New user registration with profile information
- **Logout**: Session termination

### Role-Based Access Control

- **User Roles**: Admin, Employee, Manager, Client
- **Permission Restrictions**: Different access permissions for each role
- **Automatic Redirects**: Users redirected to appropriate dashboards based on role
- **Middleware Protection**: Security middleware restricts access to unauthorized sections

### Employee Approval System

- **Pending Status**: New employees start with pending approval status
- **Admin Notifications**: Admins see pending approval counts and details
- **Approval Interface**: Simple approval/rejection buttons for each pending user
- **Waiting Screen**: Pending employees see a waiting status screen
- **Email Integration**: Automatic emails sent upon approval/rejection (coming soon)

### Dashboard

- **Role-Specific Dashboards**: Separate dashboards for admin and employees
- **Summary Statistics**: Project metrics at a glance
- **Quick Access**: Links to all app features
- **Project Status Overview**: View all projects in one place
- **Data Visualization**: Project metrics (coming soon)

### Project Management

- **Project Creation**: Add new projects with detailed information
- **Team Assignment**: Assign teams to projects
- **Department Organization**: Organize projects by department
- **Status Tracking**: Track project status (active, completed, on hold, cancelled)
- **Health Monitoring**: Project health status (good, needs work, poor)

### Project Health

- **Status Tracking**: Regular health status updates
- **Health Voting**: System for team feedback
- **Comments**: Add explanations for health assessments
- **Historical Records**: Track status changes over time

### Chat System

- **Team Communication**: Real-time messaging interface
- **Project Discussions**: Organize chats by project
- **Admin Communications**: Direct communication with team members

### User Management

- **Profile Management**: Update personal information
- **Password Management**: Securely change passwords
- **Role Assignment**: Assign appropriate roles to users
- **Company Association**: Associate users with companies

### Company Management

- **Company Creation**: Admins can create companies
- **Access Codes**: Secure codes for employee registration
- **Employee Management**: Approve/reject employee access
- **Organizational Structure**: Manage departments and teams

### Admin Dashboard

- **User Management**:
  - View all users
  - Add/edit/delete users
  - Approve/reject new employees
  - Assign roles
- **Project Management**:
  - Create new projects
  - Edit project details
  - Delete projects
  - Track project health
- **System Settings**:
  - Configure application settings
  - Manage email notifications
- **Activity Logs**:
  - Monitor user actions
  - Track system events

## Running the Project

1. **Ensure you're in the project directory with the virtual environment activated**

2. **Start the development server**

```bash
python manage.py runserver
```

3. **Access the application**

Open your web browser and navigate to:
```
http://127.0.0.1:8000/
```

This will redirect you to the login page. If you're a new user, click "Sign Up" to create an account.

### Running on a Different Port

To run the server on a different port (e.g., 8080):

```bash
python manage.py runserver 8080
```

### Accessing the Admin Interface

Django's built-in admin interface is available at:
```
http://127.0.0.1:8000/admin/
```

Use the superuser credentials created during installation to log in.

## User Guide

### Authentication

- **Login**: Navigate to `/login/` and enter your email and password
- **Sign Up**: Navigate to `/signup/` and complete the registration form
  - **Admin Role**: Create a new company
  - **Employee/Manager Role**: Join existing company with access code
  - **Client Role**: Register without company affiliation
- **Logout**: Click the "Log Out" button in the sidebar

### Employee Registration Process

1. **Sign Up**: Complete the registration form with your details
2. **Company Details**: Enter company name and access code (provided by admin)
3. **Submission**: Submit registration form
4. **Waiting for Approval**: View waiting screen while admin reviews application
5. **Access Granted**: Once approved, gain full access to the system

### Company Administration

1. **Create Company**: Register as an admin and create your company
2. **View Access Code**: Access the company code from the company code page
3. **Share Code**: Distribute the code to employees for registration
4. **Approve Employees**: Review and approve employee registrations
5. **Manage Users**: Maintain user accounts through admin dashboard

### Dashboard

Navigate to `/dashboard/` to view:
- Project statistics
- Active projects
- Team member count
- Project listings with details

### Project Health

Navigate to `/project-health/` to:
- Update project health status
- Add comments and justifications
- View status history

### Chat

Navigate to `/chat/` to:
- Send messages to team members
- View conversation history
- Discuss project-related topics

### Settings

Navigate to `/settings/` to:
- Update personal information
- Change password
- View company information

### Admin Dashboard

Navigate to `/admin-dashboard/` to access:
- User management tools
- Employee approval interface
- Project administration
- System settings
- Activity logs

## Troubleshooting

### Common Issues

1. **Missing Dependencies**
   - Error: `ModuleNotFoundError: No module named 'django'`
   - Solution: Make sure you've installed all dependencies with `pip install django django-crispy-forms`

2. **Database Migrations**
   - Error: `no such table: main_app_model`
   - Solution: Run `python manage.py migrate` to apply all migrations

3. **Static Files Not Loading**
   - Error: CSS or JavaScript not being applied
   - Solution: Make sure DEBUG=True in settings.py during development

4. **Permission Issues**
   - Error: Access denied to certain pages
   - Solution: Ensure you're logged in with the appropriate user account and role

5. **Employee Approval**
   - Issue: Employee registered but can't access dashboard
   - Solution: Admin must approve the employee from the admin dashboard

### Getting Help

If you encounter issues not covered in this documentation, please:
1. Check Django's official documentation: https://docs.djangoproject.com/
2. Open an issue on the project's GitHub repository
3. Contact the project maintainers 