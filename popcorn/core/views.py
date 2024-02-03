from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Profile, Movie
from django.contrib.auth.decorators import login_required
from django.db.models import F
from itertools import chain

# Create your views here.

@login_required(login_url='login')
def index(request):
    Movies = Movie.objects.all()
    user_profile = Profile.objects.get(user=request.user)
    print(user_profile.filmOn)
    movie_on = Movies[user_profile.filmOn]
    in_list = movie_on in user_profile.watchlist.all()
    return render(request, 'index.html', {'movie_on': movie_on, 'in_list': in_list, 'user_profile': user_profile})

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
                return redirect('index')
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
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        if request.FILES.get('profilePicture') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
        if request.FILES.get('profilePicture') != None:
            image = request.FILES.get('profilePicture')
            bio = request.POST['bio']
        user_profile.profileimg = image
        user_profile.bio = bio
        user_profile.save()
        
        return redirect('settings')
    return render(request, 'settings.html', {'user_profile': user_profile})

@login_required(login_url='login')
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)

    context = {
        'user_object': user_object,
        'user_profile': user_profile
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def next_movie(request):
    user_profile = Profile.objects.get(user=request.user)
    if user_profile.filmOn < len(Movie.objects.all())-1:
        user_profile.filmOn = user_profile.filmOn + 1
    user_profile.save()
    print(user_profile.filmOn)
    return redirect('index')

@login_required(login_url='login')
def prev_movie(request):
    user_profile = Profile.objects.get(user=request.user)
    if user_profile.filmOn > 0:
        user_profile.filmOn = user_profile.filmOn - 1
    user_profile.save()
    print(user_profile.filmOn)
    return redirect('index')

@login_required(login_url='login')
def my_list(request):
    user_profile = Profile.objects.get(user=request.user)
    return render(request, 'my_list.html', {'user_profile': user_profile, 'wlist': user_profile.watchlist.all()})

@login_required(login_url='login')
def add_movie(request):
    user_profile = Profile.objects.get(user=request.user)
    Movies = Movie.objects.all()
    movie = Movies[user_profile.filmOn]
    if movie not in user_profile.watchlist.all():
        user_profile.watchlist.add(movie)
    return redirect('index')

def remove_movie(request):
    user_profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        for movie in user_profile.watchlist.all():
            print('hello')
            if movie.title in request.POST.keys():
                user_profile.watchlist.remove(movie)
    return redirect('my_list')

def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)
    if request.method == 'POST':
        username = request.POST['search']
        title = request.POST['search']

        username_object = User.objects.filter(username__icontains=username)
        movie_object = Movie.objects.filter(title__icontains=title)

        username_profile = []
        username_profile_list = []

        title_movie = []
        title_movie_list = []

        for users in username_object:
            username_profile.append(users.id)
        
        for ids in username_profile:
            profile_list = Profile.objects.filter(id_user = ids)
            username_profile_list.append(profile_list)

        for film in movie_object:
            title_movie.append(film.title)
        
        for titles in title_movie:
            film_list = Movie.objects.filter(title = titles)
            title_movie_list.append(film_list)

        title_movie_list = list(chain(*title_movie_list))
        titles_length = len(title_movie_list)
        
        username_profile_list = list(chain(*username_profile_list))
        results_length = len(username_profile_list)

        context = {'user_profile': user_profile, 
                   'username_profile_list': username_profile_list, 
                   'results_length': results_length,
                   'title_movie_list': title_movie_list, 
                   'titles_length': titles_length}
    return render(request, 'search.html', context)

@login_required(login_url='login')
def my_profile(request):
    user_profile = Profile.objects.get(user=request.user)
    context = {
        'user_profile': user_profile
    }
    return render(request, 'profile2.html', context)