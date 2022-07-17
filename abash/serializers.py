from rest_framework import serializers
from abash.models import *
from django.contrib.auth.models import User

class LoginSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style = {'input_type': 'password'}, write_only = True)
    class Meta:
        model = User
        fields = ['username','email','password','password2'] 
        extra_kwargs = {
            'password': {'write_only': True}
        }
    def save(self):
        password = self.validated_data['password']
        password2 = self.validated_data['password2']

        if password != password2:
            raise serializers.ValidationError({'error': 'P1 and P2 should be same'})
        
        if User.objects.filter(email= self.validated_data['email']).exists():
            raise serializers.ValidationError({'error': 'Email already exists!'})

        account = User(email=self.validated_data['email'],username= self.validated_data['username'])
        account.set_password(password)
        account.save()
        return account

class UserSerialzer(serializers.Serializer):
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    profile_pic = serializers.ImageField()
    email = serializers.EmailField()
    phone = serializers.CharField()
    birth_date = serializers.DateField()
    nid_number = serializers.CharField()
    nid_file = serializers.FileField()

    
    
    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.profile_pic = validated_data.get('profile_pic', instance.profile_pic)
        instance.email = validated_data.get('email', instance.email)
        instance.phone = validated_data.get('phone', instance.phone)
        instance.birth_date = validated_data.get('birth_date', instance.birth_date)
        instance.nid_number = validated_data.get('nid_number', instance.nid_number)
        instance.nid_file = validated_data.get('nid_file', instance.nid_file)
        instance.save()
        return instance

class PropertySerializer(serializers.ModelSerializer):
    class Meta:
        model= Property
        fields = ['id','owner','home_type','rental_type','property_image','rent','area_sqft','agreement','floor','negotiable','rented']


class PropertyImagesSerializer(serializers.ModelSerializer):
    class Meta:
        model= Property_Images
        fields = ['property','more_images']

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model= Room
        fields=['property','bedroom_no','bathroom_no','drawing_dining_no','balcony_no']

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model= Location
        fields = ['property','flat','house','road','area','ward','upazila','district','division','latitude','longitude']

class RequestedBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Requested_Booking
        fields = ['id','user','property','agreement_type','start_date','end_date','rejected']

class ReceivedBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Received_Booking
        fields = ['id','owner','property','requested_user','agreement_type','start_date','end_date']

class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ['user','property']

class PropertyRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model= Property_rating
        fields = ['user','property','rating','review']

class AppRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model= App_rating
        fields = ['user','rating','review']


class FilterSerializer(serializers.Serializer):
    district = serializers.CharField(max_length=50)
    rental_type=serializers.CharField(allow_null=True,max_length=50)
    home_type = serializers.CharField(allow_null=True,max_length=50)
    rent_min = serializers.IntegerField(allow_null=True)
    rent_max = serializers.IntegerField(allow_null=True)
    area_sqft = serializers.DecimalField(allow_null=True,max_digits=9, decimal_places=2)
    bedroom_no = serializers.IntegerField(allow_null=True)
    bathroom_no = serializers.IntegerField(allow_null=True)
    drawing_dining_no = serializers.IntegerField(allow_null=True)
    balcony_no = serializers.IntegerField(allow_null=True)
