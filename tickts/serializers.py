from rest_framework import serializers 
from .models import Guest ,Movie, Post, Reservation 




class MovieSerializer (serializers.ModelSerializer):
    class Meta:
        model= Movie
        fields="__all__"



class ReservationSerializer (serializers.ModelSerializer):
    class Meta:
        model= Reservation
        fields="__all__"

class PostSerializer (serializers.ModelSerializer):
    class Meta:
        model= Post
        fields="__all__" 

class GuestSerializer (serializers.ModelSerializer):
    class Meta:
        model= Guest
        fields=['reservation','name','mobile'] 