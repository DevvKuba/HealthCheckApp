from django import template
from django.template.defaultfilters import stringfilter
from django.db.models import QuerySet

register = template.Library() 

@register.filter
def unread_comments_count(projects, user=None):
    """
    Returns the count of unread comments across all projects for a user
    
    Usage: {{ user.projects.all|unread_comments_count:user }}
    """
    count = 0
    
    if not projects or not user:
        return count
        
    # Handle both single project and querysets
    if not isinstance(projects, QuerySet):
        projects = [projects]
    
    for project in projects:
        # Get all comments for this project
        try:
            for comment in project.comments.all():
                # Check if the user has not read this comment
                if not comment.read_by.filter(id=user.id).exists():
                    count += 1
        except AttributeError:
            # Skip if this project doesn't have comments attribute
            continue
    
    return count

@register.filter
def contains(value, arg):
    """
    Returns whether the value contains the argument
    
    Usage: {{ comment.read_by.all|contains:user }}
    """
    return arg in value 