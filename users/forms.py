from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms

class RegisterFrom(UserCreationForm):
    class Meta:
        form = User
        fields = ['username','first_name','last_name','password1','password2','email']

class CustomRegisterFrorm(forms.ModelForm):
    password1 = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['username','first_name','last_name','password1','confirm_password','email']
    
    def clean(self):  # non field error
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        confirm_password = cleaned_data.get('confirm_password')

        if password1 and confirm_password and password1 != confirm_password:
            raise forms.ValidationError("Password do not match")
        
        return cleaned_data