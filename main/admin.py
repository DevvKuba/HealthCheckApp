from django.contrib import admin
from .models import ToDoList, Item, Department, Team, Project, ProjectComment

# Custom admin classes
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'team', 'department', 'status', 'health', 'start_date', 'created_by')
    list_filter = ('status', 'health', 'team', 'department')
    search_fields = ('name', 'description')
    date_hierarchy = 'created_at'
    filter_horizontal = ('members',)

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'department')
    list_filter = ('department',)
    search_fields = ('name', 'code')

class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

class ProjectCommentAdmin(admin.ModelAdmin):
    list_display = ('project', 'user', 'created_at')
    list_filter = ('project', 'user')
    search_fields = ('text',)

# Register your models here.
admin.site.register(ToDoList)
admin.site.register(Item)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(ProjectComment, ProjectCommentAdmin)
