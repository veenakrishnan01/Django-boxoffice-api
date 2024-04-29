from django import forms
from django.shortcuts import render
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import AllowAny
from rest_framework.status import HTTP_200_OK,HTTP_400_BAD_REQUEST,HTTP_404_NOT_FOUND
from rest_framework.authtoken.models import Token
from .forms import MovieForm,TicketForm
from .forms import CustomUserCreationForm
from .models import Movie,Ticket
from .serializers import MovieSerializer,TicketSerializer
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags



@api_view(['POST'])
@permission_classes((permissions.AllowAny,))
def signup(request):
    form = CustomUserCreationForm(data=request.data)
    if form.is_valid():
        form.save()
        return Response("account created successfully", status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)



@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    username = request.data.get("email")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'}, status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'}, status=HTTP_404_NOT_FOUND)
    # Determine the role of the user
    role = 'user'
    if user.is_superuser:
        role = 'admin'
    token, _ = Token.objects.get_or_create(user=user)
    response_data = {'token': token.key, 'role': role}
    if role == 'user':
        response_data['user'] = {
            'name': user.get_full_name(),
            'username': user.username,
            'email': user.email,
        }
    return Response(response_data, status=HTTP_200_OK)


@api_view(['POST'])
@permission_classes((AllowAny,))
def add_movie(request):
    form = MovieForm(data=request.data)
    if form.is_valid():
        movie = form.save()
        return Response({'id': movie.id}, status=status.HTTP_201_CREATED)
    return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes((AllowAny,))
def list_movie(request):
    movies = Movie.objects.all()
    serializer = MovieSerializer(movies, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes((AllowAny,))
def get_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    
    serializer = MovieSerializer(movie)
    return Response(serializer.data)
    

@api_view(['PUT'])
@permission_classes((AllowAny,))
def update_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)
    form = MovieForm(request.data, instance=movie)
    if form.is_valid():
        form.save()
        serializer = MovieSerializer(movie)
        return Response(serializer.data)
    else:
        return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['DELETE'])
@permission_classes((AllowAny,))
def delete_movie(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    movie.delete()
    return Response("deleted successfully")



@api_view(['GET'])
@permission_classes((AllowAny,))
def activate_movie(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    
    movie.is_active = True
    movie.save()
    
    return Response({'message': 'Movie activated successfully'}, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes((AllowAny,))
def deactivate_movie(request, pk):
    try:
        movie = Movie.objects.get(pk=pk)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)
    
    movie.is_active = False
    movie.save()
    
    return Response({'message': 'Movie deactivated successfully'}, status=status.HTTP_200_OK)




@api_view(['POST'])
@permission_classes((AllowAny,))
def book_ticket(request):
    # Extract data from the request object
    movie_id = request.data.get('movieId')
    movieName = request.data.get('movieName')
    date = request.data.get('date')
    time = request.data.get('time')
    seat_row = request.data.get('seat_row')
    seat_number = request.data.get('seat_number')
    price = request.data.get('price')
    username = request.data.get('userName')
    email = request.data.get('email')
    name = request.data.get('name')

    # Validate required fields
    if not all([movie_id, date, time, seat_row, seat_number, price, username, email, name]):
        return Response({'error': 'Please provide all required fields'}, status=status.HTTP_400_BAD_REQUEST)

    # Find the movie
    try:
        movie = Movie.objects.get(pk=movie_id)
    except Movie.DoesNotExist:
        return Response({'error': 'Movie not found'}, status=status.HTTP_404_NOT_FOUND)

    # Create a new ticket
    ticket = Ticket.objects.create(
        movie_id=movie_id,
        movieName=movieName,
        date=date,
        time=time,
        seat_row=seat_row,
        seat_number=seat_number,
        price=price,
        username=username,
        email=email,
        name=name
    )
    # Send booking confirmation email
    subject = 'Booking Confirmation'
    message = render_to_string('booking_confirmation_email.html', {'ticket': ticket})
    plain_message = strip_tags(message)
    sender_email = 'veenagkrishna01@gmail.com'
    receiver_email = request.data.get('email')
    send_mail(subject, plain_message, sender_email, [receiver_email], html_message=message)


    # Decrease available tickets count
    movie.save()

    # Serialize the ticket data
    serializer = TicketSerializer(ticket)
    return Response(serializer.data, status=status.HTTP_201_CREATED)



@api_view(['GET'])
@permission_classes((AllowAny,))
def get_mybookings(request, username):
    tickets = Ticket.objects.filter(username=username)
    serializer = TicketSerializer(tickets, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    
