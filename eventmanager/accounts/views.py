from django.shortcuts import redirect
from django.shortcuts import render

from django.http import HttpResponse

from django.urls import reverse

from accounts.forms import LoginForm
from accounts.forms import SignUpForm

from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User


def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    auth_login(request, user)
                    return render(request, 'accounts/index.html')
            else:
                context = {'form': form, 'wrong_credentials': True}
                return render(
                    request,
                    'accounts/login.html',
                    context
                )
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'accounts/index.html')


def signout(request):
    logout(request)
    return render(request, 'accounts/index.html')


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return render(request, 'accounts/index.html')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
