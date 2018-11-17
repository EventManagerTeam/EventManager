from accounts.forms import LoginForm
from accounts.forms import SignUpForm
from accounts.forms import ChangeEmailForm
from accounts.forms import AccountDetailsForm

from django.contrib import messages


from django.contrib.auth import authenticate
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash

from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import PasswordChangeForm

from django.contrib.auth.models import User

from django.shortcuts import redirect
from django.shortcuts import render

from accounts.models import AccountDetails


def index(request):
    return render(request, 'accounts/index.html')


def login(request):
    form = LoginForm(request.POST or None)
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

    return render(request, 'accounts/login.html', {'form': form})


@login_required
def home(request):
    return render(request, 'accounts/index.html')


@login_required
def signout(request):
    logout(request)
    return render(request, 'accounts/index.html')


def signup(request):
    form = SignUpForm(request.POST or None)
    if form.is_valid():
        form.save()
        username = form.cleaned_data.get('username')
        raw_password = form.cleaned_data.get('password1')
        user = authenticate(username=username, password=raw_password)
        auth_login(request, user)
        return render(request, 'accounts/index.html')

    return render(request, 'accounts/signup.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)

            success_message = 'Your password was successfully updated!'
            messages.success(request, success_message)

            return redirect('change_password')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(
        request,
        'accounts/change_password.html',
        {
            'form': form
        }
    )


@login_required
def change_email(request):
    form = ChangeEmailForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            User.objects.filter(
                email=form.cleaned_data.get('original_email')
            ).update(email=form.cleaned_data.get('new_email'))
            success_message = 'Your email was successfully updated!'
            messages.success(request, success_message)
        else:
            messages.error(request, 'Please correct the errors below.')

    return render(request, 'accounts/change_email.html', {'form': form})


def has_already_added_account_info(username):
    try:
        user = User.objects.all().get(username=username)
        AccountDetails.objects.get(user=user)
        return True
    except User.DoesNotExist or AccountDetails.DoesNotExist:
        return False


@login_required
def account_details(request):
    form = AccountDetailsForm(request.POST or None)

    if has_already_added_account_info(request.user) != 0:
        context = {'error_message': "Details were already added."}
        return render(request, 'CRUDops/error.html', context)

    if request.method == 'POST':
        if form.is_valid():
            details = form.save(commit=False)
            details.user = request.user
            if request.POST.get('birthdate'):
                details.birth_date = request.POST.get('birthdate')
            details.save()

    context = {'form': form}
    return render(
        request,
        'accounts/additonal_account_information.html',
        context
    )
