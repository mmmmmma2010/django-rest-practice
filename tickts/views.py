
from django.http import Http404
from django.http.response import JsonResponse

from .serializers import GuestSerializer , MovieSerializer ,ReservationSerializer,PostSerializer
from tickts.models import Guest, Movie, Post, Reservation
from rest_framework import status,mixins, generics,viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAutherOrReadonly



# Create your views here.


 # first type of views
def no_rest_no_model(request):
    guest =[ 
        {
            'id':1,
            "name":"mohamed",
            "mobile":123113,
        },

        {
            'id':2,
            "name":"ali",
            "mobile":3113,
        }
    ]
    return JsonResponse(guest,safe=False)


# secont type of views
def no_rest_from_model(request):
    data=Guest.objects.all()
    response={
        "guests":list(data.values("name","mobile"))
    }
    return JsonResponse(response)


#Third type of views
@api_view(["GET","POST"])
def FBV_list(request):

    #GET  
    if request.method == "GET":
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(serializer.data)

    #POST
    if request.method=="POST":
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)




@api_view(["GET","PUT",'DELETE'])
def FBV_pk(request,pk):

    guest=Guest.objects.get(pk=pk)

    #GET  
    if request.method == "GET":
        serializer=GuestSerializer(guest)
        return Response(serializer.data)

    #PUT
    if request.method=="PUT":
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        #DELETE  
    if request.method == "DELETE":
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



#fourth type of views

class CBV_list(APIView):
    def get(self,request):
        guests=Guest.objects.all()
        serializer=GuestSerializer(guests,many=True)
        return Response(serializer.data)

    def post(self,request):
        serializer=GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)




class CBV_pk(APIView):
    def get_object(self,pk):
        try:
            guest=Guest.objects.get(pk=pk)
            return guest
        except Guest.DoesNotExist:
            raise Http404

    def get(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest)
        return Response(serializer.data)

    def put(self,request,pk):
        guest=self.get_object(pk)
        serializer=GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request,pk):
        guest=self.get_object(pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

#Fifth type of views

class Mixin_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer

    def get (self,request):
        return self.list(request)
    
    def post (self ,request):
        return self.create(request)



class Mixin_pk(mixins.UpdateModelMixin,mixins.RetrieveModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer

    def put (self,request,pk):
        return self.update(request)

    def get (self,request,pk):
        return self.retrieve(request)

    def delete (self,request,pk):
        return self.destroy(request)    

#sixth type of views
class Genirics_list(generics.ListCreateAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer

class Genirics_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer
    authentication_classes=[TokenAuthentication]
    permission_classes=[IsAutherOrReadonly]


#seventh type of views
class viewsets_guest(viewsets.ModelViewSet):
    queryset=Guest.objects.all()
    serializer_class=GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset=Movie.objects.all()
    serializer_class=MovieSerializer

class viewsets_reservation(viewsets.ModelViewSet):
    queryset=Reservation.objects.all()
    serializer_class=ReservationSerializer

####################Search################
@api_view(["GET"])
def find_movie(request):
    movies=Movie.objects.filter(hall=request.data['hall'],movie=request.data['movie'])
    serializer=MovieSerializer(movies,many=True)
    return Response(serializer.data,status=status.HTTP_302_FOUND)

###############create Reservation#########################
@api_view(["POST"])
def new_reservation(request):


    movie=Movie.objects.filter(movie=request.data['movie']).first()

    guest=Guest()
    guest.name=request.data['name']
    guest.mobile=request.data['mobile']
    guest.save()

    reservation=Reservation()
    reservation.guest=guest
    reservation.movie=movie
    reservation.save()

    return Response(status= status.HTTP_201_CREATED)





class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    queryset=Post.objects.all()
    serializer_class=PostSerializer
    # authentication_classes=[TokenAuthentication]
    permission_classes=[IsAutherOrReadonly]
