from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Profile, Avatar


class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={'placeholder': 'Username'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Last name'}))
    email = forms.EmailField(max_length=200, widget=forms.TextInput(attrs={'placeholder': 'Email'}))

    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise ValidationError("Username already exists")
        elif username=='followers' or username=='search':
            raise ValidationError("Try another username")
        return username

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2',)


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date',)
        widgets = {
            'birth_date': forms.DateTimeInput(attrs={'class': 'datetime-input'})
        }


class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Avatar
        fields = ('image',)


class TagForm(forms.Form):
    new_tags = forms.CharField(label='New tag(s)', max_length=200)
