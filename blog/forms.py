from django import forms
from .models import Post, Profile, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from captcha.fields import CaptchaField


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'content', 'read_time', 'image')


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30,required=True)
    last_name = forms.CharField(max_length=30,required=True)
    email = forms.EmailField(max_length=254, required=True)
    birth_date = forms.DateField(required=True, help_text='Required. Format: YYYY-MM-DD')
    country = forms.CharField(max_length=30, required=True)
    captcha = CaptchaField()

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'birth_date', 'country', 'email', 'password1', 'password2')


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('bio', 'birth_date', 'country', 'profile_picture')


class CommentForm(forms.ModelForm):
    captcha = CaptchaField()

    class Meta:
        model = Comment
        fields = ('author', 'text',)


class ContactForm(forms.Form):
    from_email = forms.EmailField(required=True)
    subject = forms.CharField(required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)
    captcha = CaptchaField()