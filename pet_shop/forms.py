from django import forms
from django.contrib.auth.models import User
from .models import *

class UserCreateForm(forms.ModelForm):
    #extra field
    password_confirm = forms.CharField(widget=forms.PasswordInput(attrs={
                'class':'form-control mb-1',
                'placeholder': 'confirm password'}), 
                required=True)

    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'last_name'
        ]
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Username'
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'password'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control mb-1',
                'placeholder': 'Full Name',
                'required': 'true'
            }),                    
        }

    # remove the help text
    def __init__(self, *args, **kwargs):
        super(UserCreateForm, self).__init__(*args, **kwargs)

        for fieldname in []:
            self.fields[fieldname].help_text = None


class PetCreateForm(forms.ModelForm):
    new_type = forms.CharField(widget=forms.TextInput(attrs={
                'maxlength':'20',
                'placeholder': 'New Pet Type'}),
                required=False)
    new_color = forms.CharField(widget=forms.TextInput(attrs={
                'maxlength':'20',
                'placeholder': 'New Pet Color'}),
                required=False)
    class Meta:
        model = Pet
        fields = [
            'name',
            'birth',
            'gender',
            'weight',
            'color',
            'description',
            'type',
            'image',
        ]

    # remove the help text
    def __init__(self, *args, **kwargs):
        super(PetCreateForm, self).__init__(*args, **kwargs)
        for fieldname in self.fields:
            self.fields[fieldname].help_text = None
            if fieldname == "weight":
                self.fields[fieldname].widget.attrs['min'] = '0'

            if fieldname != "image":
                self.fields[fieldname].widget.attrs['class'] = 'form-control mb-1'
            else:
                self.fields[fieldname].widget.attrs['class'] = 'mb-1'

            self.fields[fieldname].widget.attrs['placeholder'] = fieldname
