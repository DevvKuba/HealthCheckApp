from django import forms
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Company
from django.core.exceptions import ValidationError

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    date_of_birth = forms.DateField(required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    company_name = forms.CharField(max_length=200, required=False)
    company_code = forms.CharField(max_length=20, required=False, help_text='Required for Project Manager and Employee roles')
    
    ROLE_CHOICES = [
        ('admin', 'Project Admin'),
        ('employee', 'Project Employee'),
        ('manager', 'Project Manager'),
        ('client', 'Client'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        company_name = cleaned_data.get('company_name')
        company_code = cleaned_data.get('company_code')
        
        # If role is employee or manager, company and code are required
        if role in ['employee', 'manager']:
            if not company_name:
                raise ValidationError('Company name is required for this role')
            
            # Check if company exists
            if not Company.is_valid_company(company_name):
                raise ValidationError('This company has not been registered by an admin')
            
            # Company code is required
            if not company_code:
                raise ValidationError('Company code is required for this role')
            
            # Validate company code
            if not Company.validate_code(company_name, company_code):
                raise ValidationError('Invalid company code')
        
        # If role is admin and company name exists, ensure it's not already taken
        elif role == 'admin' and company_name:
            if Company.is_valid_company(company_name):
                raise ValidationError('This company name is already registered')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            role = self.cleaned_data['role']
            company_name = self.cleaned_data.get('company_name')
            company = None
            
            # If admin is creating a new company
            if role == 'admin' and company_name:
                company = Company.objects.create(
                    name=company_name,
                    created_by=user
                )
            
            # If employee/manager is joining existing company
            elif role in ['employee', 'manager'] and company_name:
                try:
                    company = Company.objects.get(name=company_name)
                except Company.DoesNotExist:
                    pass  # This should have been caught in clean()
            
            # Determine if user should be auto-approved
            # Admins are auto-approved, employees and managers need approval
            is_auto_approved = role in ['admin', 'client']
            
            # Create UserProfile
            UserProfile.objects.create(
                user=user,
                role=self.cleaned_data['role'],
                company_name=self.cleaned_data.get('company_name'),
                company=company,
                date_of_birth=self.cleaned_data['date_of_birth'],
                is_approved=is_auto_approved
            )
            
        return user