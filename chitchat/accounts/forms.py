from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from .models import *



class Chatmessagecreateform(ModelForm):
    class Meta:
        model=Groupmessages
        fields=['body']
        widgets = {
            'body': forms.TextInput(attrs={
                'placeholder': "Add message .....",
                'class': 'messages-new',  
                'autofocus': True,
            })
        }








   
class Auth(AuthenticationForm):
    username=forms.CharField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter username'}))
    email=forms.EmailField(widget=forms.TextInput(attrs={'class':'form-control','placeholder':'enter email'}))
    password=forms.CharField(widget=forms.TextInput(attrs={'placeholder':"enter your password"}))
    




class Register(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            "class": "register-email",
            "placeholder": "Enter your email"
        })
    )
    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Enter your password",
            "class": "register-password"
        }),
        help_text=None,
    )
    password2 = forms.CharField(
        label="Confirm password",
        strip=False,
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm your password",
            "class": "register-password"
        }),
        help_text=None,
    )

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "register-username",
                "placeholder": "Enter your username"
            })
           
        }

    def __init__(self, *args, **kwargs):  # 👈 now properly indented
        super().__init__(*args, **kwargs)
        for field in ['username', 'password1', 'password2']:
            self.fields[field].help_text = None

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email.endswith("@gmail.com"):
            raise ValidationError("only gmails are allowed")
        return email
    
    def clean_password2(self):
        password1=self.cleaned_data.get("password1")
        password2=self.cleaned_data.get("password2")
        print(password1)
        print(password2)
        if not password1==password2:
            raise ValidationError("password doesnot match")
        return password2



