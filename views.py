from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import BookingDetails, WorkshopAccount
from rest_framework import serializers
from restapi.serializers import SearchSerializer, UserSerializer, WorkshopWorksSerializers
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .models import WorkshopAccount
from django.db.models import Q
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance
# Create your views here.


class RegisterView(APIView):
    permission_classes = (AllowAny,)
    def post(self,req):
        serializer = UserSerializer(data=req.data)
        if serializer.is_valid():
            user = serializer.save()
            user.first_name = req.data.get('name')
            user.save()
            token = Token.objects.create(user = user)
            return Response({'token': token.key})
        return Response(serializer.errors)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    def post(self,req):
        username = req.data.get('username')
        password = req.data.get('password')
        user = authenticate(username = username,password=password)
        content = {}
        if user is not None:
            token,create = Token.objects.get_or_create(user = user)
            content['token'] = token.key
            content['name'] = user.first_name
            return Response(content)
        return Response({'err': 'Invalid Credentials'}) 



class HomeView(APIView):
    permission_classes = (AllowAny,)
    def get(self,req):
        print(req.META.get('HTTP_AUTHORIZATION'))
        user = Token.objects.get(key = req.META.get('HTTP_AUTHORIZATION')[6:]).user        
        content = {}         
        content['username'] = user.username
        content['name'] = user.first_name
        return Response(content)

class WorkshopHomeView(APIView):
    permission_classes = (AllowAny,)
    def get(self,req):
        print(req.META.get('HTTP_AUTHORIZATION'))
        user = Token.objects.get(key = req.META.get('HTTP_AUTHORIZATION')[6:]).user        
        content = {}         
        content['username'] = user.username
        content['name'] = WorkshopAccount.objects.get(user = user).workshopName
        return Response(content)
        

class SearchView(APIView):
    permission_classes = (AllowAny,)
    def get(self,req):
        query = req.GET.get('query')
        # print(query)
        queryset = WorkshopAccount.objects.filter(Q(address__icontains = query) | Q(workshopName__icontains = query) )
        # print(queryset)
        serializers = SearchSerializer(queryset,many=True)
        return Response(serializers.data)


class NearbyWorkshops(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self,req):
        lat = float(req.data.get('lat'))
        lon = float(req.data.get('lon'))
        radius = 10
        loc = Point(lon,lat)
        print(lat,lon,loc)
        # queryset = WorkshopAccount.objects.filter(location__dwithin=(loc,10))    
        queryset = WorkshopAccount.objects.filter(location__distance_lt=(loc, Distance(km=radius)))
        print(queryset)
        serializers = SearchSerializer(queryset,many=True)
        return Response(serializers.data)




class BookServices(APIView):
    permission_classes = (AllowAny,)
    def post(self,req):
        user = User.objects.get(username = req.data.get('username'))
        workshop = WorkshopAccount.objects.get(user = req.data.get('uid'))
        msg = req.data.get('msg')
        lat = req.data.get('lat')
        lon = req.data.get('lon')
        booking = BookingDetails.objects.create(user = user,workshop = workshop,msg = msg)
        booking.latitude = lat
        booking.longitude = lon
        booking.save()
        content = {}
        content['user'] = user.username
        content['workshop'] = workshop.address
        content['msg'] = msg
        content['workshopUser'] = workshop.user.username
        return Response(content)


class WorkshopWorks(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self,req):
        user = Token.objects.get(key = req.META.get('HTTP_AUTHORIZATION')[6:]).user
        workshop = WorkshopAccount.objects.get(user = user)
        works = BookingDetails.objects.filter(workshop = workshop)
        content = {}
        if len(works) == 0:
            content["Works"] = "None"
            return Response(content)
        serializer = WorkshopWorksSerializers(works,many = True)
        return Response(serializer.data)

