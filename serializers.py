from django.db.models import fields
from restapi import models
from restapi.models import BookingDetails, WorkshopAccount
from django.contrib.auth.models import User
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','password','first_name']
    def create(self, validated_data):
        user = User.objects.create(
            username = validated_data.get('username'),
            email = validated_data.get('email'),
            
        )
        
        
        user.set_password(validated_data.get('password'))
        user.save()

        return user


class SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model= WorkshopAccount
        fields = ['user','workshopName','address','phone','latitude','longitude']




class WorkUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','email','first_name']

class WorkshopWorksSerializers(serializers.ModelSerializer):
    user = WorkUserSerializer()
    class Meta:
        model = BookingDetails
        fields = ['id','created','latitude','longitude','msg','user','status']