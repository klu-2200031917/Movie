from django.urls import path

from . import views

urlpatterns = [
    path('', views.index1, name='index1'),
    path('index/',views.index,name='index'),
    path('<int:movie_id>/',views.detail ,name='detail'),
    path('signup/',views.signUp,name='signup'),
    path('login/',views.Login,name='login'),
    path('logout/',views.Logout,name='logout'),
    path('recommend/',views.recommend,name='recommend'),
    path('genre/<str:genre>/', views.genre_movies, name='genre_movies'),
    path('movies/', views.movie_list, name='movie_list'),
    path('add_movie/',views.add_movie,name='add_movie'),
    path('movies/update/<int:movie_id>/', views.update_movie, name='update_movie'),
    path('movies/delete/<int:movie_id>/', views.delete_movie, name='delete_movie'),
    path('admin/',views.admin,name='admin'),
    path('movies1/',views.movie_list1,name='movie_list1'),

]