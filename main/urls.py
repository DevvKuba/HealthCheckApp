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
    path("admin-dashboard/", views.admin_dashboard, name="admin_dashboard"),
]