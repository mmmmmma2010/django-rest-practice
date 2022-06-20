
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from tickts import views
from rest_framework.authtoken.views import obtain_auth_token

router=DefaultRouter()
router.register("guests",views.viewsets_guest)
router.register("movies",views.viewsets_movie)
router.register("reservition",views.viewsets_reservation)

urlpatterns = [
    path('admin/', admin.site.urls),
    #1
    path('api/index', views.no_rest_no_model ),
    #2
    path('api/guests', views.no_rest_from_model ),
    #3
    path('api/guestslist', views.FBV_list ),
    #3
    path('api/guest/<int:pk>', views.FBV_pk ),
    #4
    path('api/guestscbv', views.CBV_list.as_view() ),

    path('api/guestcbv/<int:pk>', views.CBV_pk.as_view() ),
    #5
    path('api/guestsmixins/', views.Mixin_list.as_view() ),
    path('api/guestsmixins/<int:pk>', views.Mixin_pk.as_view() ),

    #6
    path('api/guestsgeniric/', views.Genirics_list.as_view() ),
    path('api/guestsgeniric/<int:pk>', views.Genirics_pk.as_view() ),
    #7
    path('api/viewsets/', include(router.urls) ),
    #Find movies
    path('api/findmoviefbv', views.find_movie ),
    #New Reservation 
    path('api/addreservationfbv', views.new_reservation ),
    #rest auth url
    path('api-auth', include('rest_framework.urls') ),
    # rest token auth
    path('api-token-auth', obtain_auth_token ),
    

    #post urls
    path('api/postsgeniric/<int:pk>', views.Post_pk.as_view() ),

]