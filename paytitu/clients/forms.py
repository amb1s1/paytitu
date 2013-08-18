from django import forms
from django.forms import ModelForm
from django.forms import PasswordInput, extras

class loginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=PasswordInput())
    
    
class ProfileForm(forms.Form):
    firstname = forms.CharField(max_length=100)
    lastname = forms.CharField(max_length=100)
    #email = forms.EmailField(max_length=100)
    location = forms.CharField(max_length=100)
    interest = forms.CharField(max_length=244)
    contact = forms.CharField(max_length=100)
    
    
    # form.is_valid() is triggers cleaned_data function of a form.
    # Raise validation error if the condition is not met.
   
    ### Cleaning a specific field attribute ### 
    def cleaned_firstname(self):
        data = self.cleaned_data['firstname']
        
        if data is None:
            raise forms.ValidationError("You must enter first name.")
        
        return data

        