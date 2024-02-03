from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('profile/logout', views.logout, name='logout'),
    path('settings', views.settings, name='settings'),
    path('profile/<str:pk>', views.profile, name='profile'),
    path('next_movie', views.next_movie, name='next'),
    path('prev_movie', views.prev_movie, name='prev'),
    path('my_list', views.my_list, name='my_list'),
    path('add_movie', views.add_movie, name='add_movie'),
    path('remove_movie', views.remove_movie, name='remove_movie'),
    path('search', views.search, name='search'),
    path('my_profile', views.my_profile, name="my_profile")

]