from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required(login_url='login')
def index(request):
    return render(request, 'index.html')

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request, 'An account with this email exists already.')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username is taken.')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #Log user in and direct to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)


                #create profile for user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('signup')
        else:
            messages.info(request, 'Passwords do not match.')
            return redirect('settings')
        
    else:
        return render(request, 'signup.html')
    
def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password incorrect.')
            return redirect('login')
    else:
        return render(request, 'login.html')
    
@login_required(login_url='login')
def logout(request):
    auth.logout(request)
    return redirect('login')

@login_required(login_url='login')
def settings(request):
    return render(request, 'settings.html')

@login_required(login_url='login')
def profile(request):
    return render(request, 'profile.html')