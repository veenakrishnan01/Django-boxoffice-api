from django.urls import path
from . import views

urlpatterns = [
  path('signup',views.signup,name='signup_api'), 
  path('login', views.login, name='login_api'),
  path('add_movie', views.add_movie, name='addmovieapi'), 
  path('list_movie', views.list_movie, name='listmovieapi'),
  path('<int:pk>/get_movie', views.get_movie, name='getmovieapi'),
  path('<int:pk>/update_movie', views.update_movie, name='updatemovieapi'),
  path('<int:pk>/delete_movie', views.delete_movie, name='deletemovieapi'),
  path('<int:pk>/activate_movie', views.activate_movie, name="activatemovie"),
  path('<int:pk>/deactivate_movie', views.deactivate_movie, name='deactivatemovie'),
  path('<str:username>/get_mybookings', views.get_mybookings, name='getmybookings'),
  path('book_ticket', views.book_ticket, name='bookticket'),
]
