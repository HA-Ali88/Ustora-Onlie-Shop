from django import forms
from django.contrib.auth.models import User

class User_Registration_Form(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput)
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']
    
    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class UserEditForm(forms.ModelForm):
    def clean_email(self):
        data = self.cleaned_data['email']
        check_email = User.objects.filter(email=data).exclude(id=self.instance.id)
        if check_email.exists():
            raise forms.ValidationError('Email already in use.')
        return data
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        