from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User

from django.shortcuts import render


def index(request):
    if request.user.is_authenticated:
        return home(request)
    return render(request, 'accounts/index.html')


@login_required
def home(request):
    return render(request, 'accounts/home.html')
