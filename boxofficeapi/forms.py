from django import forms
from .models import Movie,Ticket
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class MovieForm(forms.ModelForm):
    class Meta:
        model = Movie
        fields = ['movieName','language','actors','director','description','imageUrl','is_active','startDate', 'endDate']
        
        


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "password1", "password2")
        
        
class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['movie_id','movieName','date','time','seat_row','seat_number','price','username','email','name']
