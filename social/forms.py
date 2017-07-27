from django import forms
from social.models import User_model

class SignUp_form(forms.ModelForm):
    class Meta:
        model=User_model
        fields=['name','username','email','password']

class Login_form(forms.ModelForm):
    class Meta:
        model=User_model
        fields=['username','password']
