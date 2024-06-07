from django import forms
from .models import Profile
from django.contrib.auth.models import User
from .widgets import CustomPictureImageFieldWidget

class UserForm(forms.ModelForm):

    username = forms.CharField(disabled=True)

    class Meta:
        model = User
        fields = { 'username' }

class ProfileForm(forms.ModelForm):

    field_order = ('user','name','lastname','phone_number','photo')
    photo = forms.ImageField(widget=CustomPictureImageFieldWidget)

    class Meta:
        model = Profile
        fields = {
            'name',
            'lastname',
            'phone_number',
            'photo'
        }
