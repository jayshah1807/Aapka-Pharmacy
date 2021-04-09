from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile,Comment




class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['profile_image','date_of_birth','contact_no']

# class CommentForm(forms.ModelForm):
#     comment = forms.CharField(widget=forms.Textarea(attrs={'class': 'materialize-textare'}), required=False)
#     rate = forms.ChoiceField(widget=forms.Select(),required=True)
#     class Meta:
#         model = Comment
#         fields = ['subject','comment','rate']
