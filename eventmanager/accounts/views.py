from django.shortcuts import render
from django.shortcuts import redirect

from django.http import HttpResponse

from django.urls import reverse

from accounts.forms import SignUpForm
from accounts.forms import LoginForm

from django.contrib.auth import authenticate
from django.contrib.auth import login
from django.contrib.auth import logout

from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User


def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return reverse("accounts.index")
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
        return home(request)
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return render(request, 'accounts/index.html')

    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})
