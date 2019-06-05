from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm



# Create your views here.

def homepage_view(request):
    return HttpResponse('Hello world')

def login_view(request):
    pass

def logout_view(request):
    pass   

def register_view(request):
    
    if request.method == 'GET':

        if request.user.is_authenticated: # Redirect if current user is already logged in
            return redirect('main:homepage')

        form = UserCreationForm()
        return render(request, 'main/register.html', {'form' : form})

    if request.method == 'POST':

        form = UserCreationForm(request.POST)
        
        if form.is_valid:
            user = form.save()
            login(request, user)
            return redirect('main:homepage')