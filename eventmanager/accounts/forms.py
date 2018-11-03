from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )

    last_name = forms.CharField(
        max_length=30,
        required=False,
        help_text='Optional.'
    )
    email = forms.EmailField(max_length=254, help_text='Required.')

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        )


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={'placeholder': 'Username'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'placeholder': 'Password'})
    )
    fields = ['username', 'password']

    username.widget.attrs['class'] = 'formfield'
    password.widget.attrs['class'] = 'formfield'
