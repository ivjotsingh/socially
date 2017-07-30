from django import forms
from social.models import User_model,Post_model

class SignUp_form(forms.ModelForm):
    class Meta:
        model=User_model
        fields=['name','username','email','password']
        widgets = {'password': forms.PasswordInput() }

class Login_form(forms.ModelForm):
    class Meta:
        model=User_model
        fields=['username','password']

class Post_form(forms.ModelForm):
    class Meta:
        model=Post_model
        fields=['caption','image']
