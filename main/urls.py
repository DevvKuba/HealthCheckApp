from django.urls import path
from . import views

urlpatterns = [
    path("<int:id>", views.index, name="index"),
    path("home/", views.home, name="home"),
    path("create/", views.create, name="create"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("chat/", views.chat, name="chat"),
    path("settings/", views.settings, name="settings"),
    path("project-health/", views.project_health, name="project_health"),
    path("save-project-health/", views.save_project_health, name="save_project_health"),
    path("add-improvement/", views.add_improvement, name="add_improvement"),
    path("toggle-improvement/<int:improvement_id>/", views.toggle_improvement, name="toggle_improvement"),
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("add-project/", views.add_project, name="add_project"),
]