from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AccountCreationForm, AccountAuthentication, ProfileCreationForm


def homepage_view(request):
    return render(request, 'main/home.html', {'title': 'Home'})


def login_view(request):

    # Redirect the user if already logged in
    if request.user.is_authenticated:
        return redirect('main:homepage')

    if request.method == 'GET':
        form = AccountAuthentication()
        return render(request, 'main/login.html', {'title': 'Login', 'form': form})

    if request.method == 'POST':
        form = AccountAuthentication(data=request.POST)
        if form.is_valid():
            # email = form.cleaned_data.get('email')
            # password = form.cleaned_data.get('password')
            user = form.authenticate_via_email()

            if user is not None:
                login(request, user)
                return redirect('main:homepage')
            else:
                messages.error(
                    request, 'Account doesn\'t exist. Create one <a href="/register" class="alert-link">Here!</a>')
                return redirect('main:login')

        else:
            for error in form.error_messages:
                messages.error(request, form.error_messages[error])
            return redirect('main:login')


def logout_view(request):
    logout(request)
    return redirect('main:homepage')


def register_view(request):

    # Redirect the user if already logged in
    if request.user.is_authenticated:
        return redirect('main:homepage')

    if request.method == 'GET':
        form = AccountCreationForm()
        return render(request, 'main/register.html', {'title': 'Register', 'form': form})

    if request.method == 'POST':
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main:homepage')

        messages.error(request, 'Form not valid')
        return redirect('main:register')


@login_required(login_url='main:login')
def redirect_to_current_profile(request):

    if request.method == 'GET':
        return redirect('main:profile', username=(request.user.username))


@login_required(login_url='main:login')
def profile_view(request, username):

    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        return render(request, 'main/profile.html', {'title': user.username, 'other_user': user})


@login_required(login_url='main:login')
def search_profile(request):

    if request.method == 'GET':
        search = request.GET.get('search')
        user = User.objects.filter(username=search).first()
        if user is not None:
            return redirect('main:profile', username=(user.username))
        else:
            return redirect('main:homepage')


@login_required(login_url='main:login')
def settings(request):
    pass


@login_required(login_url='main:login')
def profile_settings(request):

    if request.method == 'GET':
        form = ProfileCreationForm()
        return render(request, 'main/profile_settings.html', {'title': 'Profile Setup', 'form': form})


@login_required(login_url='main:login')
def account_settings(request):
    pass
