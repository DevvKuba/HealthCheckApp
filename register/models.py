from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.
class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    access_code = models.CharField(max_length=20, unique=True, default=uuid.uuid4().hex[:8])
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='companies')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
        
    @classmethod
    def is_valid_company(cls, company_name):
        return cls.objects.filter(name=company_name).exists()
    
    @classmethod
    def validate_code(cls, company_name, code):
        try:
            company = cls.objects.get(name=company_name)
            return company.access_code == code
        except cls.DoesNotExist:
            return False

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Project Admin'),
        ('employee', 'Project Employee'),
        ('manager', 'Project Manager'),
        ('client', 'Client'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    company_name = models.CharField(max_length=200, blank=True, null=True)
    company = models.ForeignKey(Company, on_delete=models.SET_NULL, null=True, blank=True, related_name='employees')
    date_of_birth = models.DateField(null=True, blank=True)
    is_approved = models.BooleanField(default=False, help_text="Whether this user is approved to access the system")
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
        
    @classmethod
    def pending_count(cls, company):
        """Returns the count of pending users for a company"""
        return cls.objects.filter(company=company, is_approved=False).count()
