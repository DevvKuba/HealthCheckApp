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
│   ├── migrations/          # Database migrations
│   ├── models.py            # Data models
│   ├── templates/           # HTML templates
│   │   └── main/
│   │       ├── admin_dashboard.html
│   │       ├── base.html
│   │       ├── chat.html
│   │       ├── create.html
│   │       ├── dashboard.html
│   │       ├── home.html
│   │       ├── list.html
│   │       ├── project_health.html
│   │       └── settings.html
│   ├── tests.py
│   ├── urls.py              # App URL configuration
│   └── views.py             # View functions
├── register/                # User registration app
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py             # Registration forms
│   ├── migrations/
│   ├── models.py
│   ├── templates/           # Registration templates
│   │   └── register/
│   │       ├── login.html
│   │       ├── register.html
│   │       └── signup.html
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
| `admin-dashboard/` | `views.admin_dashboard` | `admin_dashboard` | Admin dashboard |

## Features

### Authentication System

- **Login**: Email and password-based authentication
- **Sign Up**: New user registration with profile information
- **Logout**: Session termination

### Dashboard

- Summary statistics for projects
- Quick access to all app features
- Project status overview
- Data visualization for project metrics

### Project Health

- Status tracking for projects
- Health voting system
- Comments and justifications
- Historical project status records

### Chat System

- Real-time messaging interface
- Project-related discussions
- Team communication

### Settings

- User profile management
- Password updates
- Theme customization options
- Notification preferences

### Admin Dashboard

- User management
  - View all users
  - Add/edit/delete users
  - Assign roles
- Project management
  - Create new projects
  - Edit project details
  - Delete projects
- System settings
  - Configure application settings
  - Manage email notifications
- Activity logs
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
- **Logout**: Click the "Log Out" button in the sidebar

### Dashboard

Navigate to `/dashboard/` to view:
- Project statistics
- Active projects
- Team member count
- Project listings with IDs

### Project Health

Navigate to `/project-health/` to:
- Vote on project health status
- Add comments and justifications
- View voting history

### Chat

Navigate to `/chat/` to:
- Send messages to team members
- View conversation history
- Discuss project-related topics

### Settings

Navigate to `/settings/` to:
- Update personal information
- Change password
- Customize theme preferences

### Admin Dashboard

Navigate to `/admin-dashboard/` to access:
- User management tools
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
   - Solution: Ensure you're logged in with the appropriate user account

### Getting Help

If you encounter issues not covered in this documentation, please:
1. Check Django's official documentation: https://docs.djangoproject.com/
2. Open an issue on the project's GitHub repository
3. Contact the project maintainers 