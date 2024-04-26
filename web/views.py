from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import Http404
from .models import Movie, Myrating
from django.contrib import messages
from .forms import UserForm
from django.db.models import Case, When
from .recommendation import Myrecommend
import numpy as np
import pandas as pd


# for recommendation
def recommend(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    df = pd.DataFrame(list(Myrating.objects.all().values()))
    nu = df.user_id.unique().shape[0]
    current_user_id = request.user.id
    # if new user not rated any movie
    if current_user_id > nu:
        movie = Movie.objects.get(id=15)
        q = Myrating(user=request.user, movie=movie, rating=0)
        q.save()

    print("Current user id: ", current_user_id)
    prediction_matrix, Ymean = Myrecommend()
    my_predictions = prediction_matrix[:, current_user_id - 1] + Ymean.flatten()
    pred_idxs_sorted = np.argsort(my_predictions)
    pred_idxs_sorted[:] = pred_idxs_sorted[::-1]
    pred_idxs_sorted = pred_idxs_sorted + 1
    print(pred_idxs_sorted)
    preserved = Case(*[When(pk=pk, then=pos) for pos, pk in enumerate(pred_idxs_sorted)])
    movie_list = list(Movie.objects.filter(id__in=pred_idxs_sorted, ).order_by(preserved)[:10])
    return render(request, 'web/recommend.html', {'movie_list': movie_list})


# List view
def index(request):
    movies = Movie.objects.all()
    query = request.GET.get('q')
    if query:
        movies = Movie.objects.filter(Q(title__icontains=query)).distinct()
        return render(request, 'web/list.html', {'movies': movies})
    return render(request, 'web/list.html', {'movies': movies})

def index1(request):
    return render (request,'web/home.html')
# detail view
def detail(request, movie_id):
    if not request.user.is_authenticated:
        return redirect("login")
    if not request.user.is_active:
        raise Http404
    movies = get_object_or_404(Movie, id=movie_id)
    # for rating
    if request.method == "POST":
        rate = request.POST['rating']
        ratingObject = Myrating()
        ratingObject.user = request.user
        ratingObject.movie = movies
        ratingObject.rating = rate
        ratingObject.save()
        messages.success(request, "Your Rating is submitted ")
        return redirect("index")
    return render(request, 'web/detail.html', {'movies': movies})


# Register user
def signUp(request):
    form = UserForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
    context = {
        'form': form
    }
    return render(request, 'web/signUp.html', context)


# Login User
def Login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return redirect("index")
            else:
                return render(request, 'web/login.html', {'error_message': 'Your account is disabled'})
        else:
            return render(request, 'web/login.html', {'error_message': 'Invalid Login'})
    return render(request, 'web/login.html')


# Logout user
def Logout(request):
    logout(request)
    return redirect("login")



from django.shortcuts import render
from .models import Movie



def genre_movies(request, genre):
    # Your logic for fetching and displaying movies based on the genre
    # For illustration purposes, let's assume you have a Movie model with a 'genre' field

    # Fetch movies based on the genre
    movies = Movie.objects.filter(genre=genre)

    # You can add more complex logic here, such as sorting, filtering, etc.

    context = {'genre': genre, 'movies': movies}
    return render(request, 'web/genre_movies.html', context)


from django.shortcuts import render
from .models import Movie, Myrating

def movie_list(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies
    }
    return render(request, 'web/movie_list.html', context)

def movie_list1(request):
    genre = request.GET.get('genre')
    if genre:
        movies = Movie.objects.filter(genre=genre)
    else:
        movies = Movie.objects.all()

    context = {
        'movies': movies
    }
    return render(request, 'web/movie_list1.html', context)

from django.shortcuts import render, redirect
from .models import Movie

# Example view for adding a movie
def add_movie(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        genre = request.POST.get('genre')
        movie_logo=request.FILES.get('movie_logo')
        movie = Movie.objects.create(title=title, genre=genre  , movie_logo=movie_logo)
        return redirect('movie_list')
    return render(request, 'web/add_movie.html')

# Similar views for updating and deleting movies
# views.py

from django.shortcuts import render, redirect, get_object_or_404
from .models import Movie
from .forms import MovieForm  # Import the form for handling movie data

def update_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        form = MovieForm(request.POST, request.FILES, instance=movie)
        if form.is_valid():
            form.save()
            return redirect('movie_list')
    else:
        form = MovieForm(instance=movie)
    context = {'form': form, 'movie': movie}
    return render(request, 'web/update_movie.html', context)


def delete_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    if request.method == 'POST':
        movie.delete()
        return redirect('movie_list')
    context = {'movie': movie}
    return render(request, 'web/delete_movie.html', context)


def admin(request):
    return render(request,'web/admin.html')