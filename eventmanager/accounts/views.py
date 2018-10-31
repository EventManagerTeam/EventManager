from django.shortcuts import render
from django.http import HttpResponse

from accounts.forms import SignUpForm

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login

def index(request):
    return render(request, 'accounts/index.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return HttpResponse(User.objects.all())
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})