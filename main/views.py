from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


def homepage_view(request):
    return render(request, 'main/home.html')


def login_view(request):

    # Redirect the user if already logged in
    if request.user.is_authenticated:
        return redirect('main:homepage')


    if request.method == 'GET':        
        form = AuthenticationForm()
        return render(request, 'main/login.html', {'form' : form})


    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('main:homepage')
            else:
                return redirect('main:login')

        else:
            for error in form.error_messages:
                print(form.error_messages[error])
            return redirect('main:login')


def logout_view(request):
    logout(request)
    return redirect('main:homepage')   


def register_view(request):

    # Redirect the user if already logged in
    if request.user.is_authenticated:
        return redirect('main:homepage')


    if request.method == 'GET':
        form = UserCreationForm()
        return render(request, 'main/register.html', {'form' : form})


    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            user = form.save()
            login(request, user)
            return redirect('main:homepage')


def redirect_to_current_profile(request):

    # Redirect the user if he hasnt logged in yet    
    if not request.user.is_authenticated:
        return redirect('main:login')

    
    if request.method == 'GET':
        return redirect('main:profile', username=(request.user.username))


def profile_view(request, username):
    
    # Redirect the user if he hasnt logged in yet
    if not request.user.is_authenticated:
        return redirect('main:login')
    

    if request.method == 'GET':
        user = User.objects.filter(username=username).first()
        return render(request, 'main/profile.html', {'user' : user})

def search_profile(request):

    # Redirect the user if he hasnt logged in yet
    if not request.user.is_authenticated:
        return redirect('main:login')

    
    if request.method == 'GET':
        search = request.GET.get('search')
        user = User.objects.filter(username=search).first()
        if user is not None:
            return redirect('main:profile', username=(user.username))
        else:
            return redirect('main:homepage')