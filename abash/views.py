from django.shortcuts import render
from rest_framework.response import Response
from abash.models import *
from abash.serializers import *
from rest_framework.decorators import api_view,permission_classes
from django.db import transaction
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.db.models import Q
# Create your views here. 
#Login Create
@api_view(['POST'])
def login_create(request):
    if request.method == 'POST':
        serializer = LoginSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            with transaction.atomic():
                user_instance = serializer.save()
                User_Details.objects.create(user= user_instance,first_name = user_instance.username, email=user_instance.email)

                data['response'] = "Registration Successful!"
                data['username'] = user_instance.username
                data['email'] = user_instance.email
                token = Token.objects.get(user=user_instance).key
                data['token'] = token

        else:
            data = serializer.errors
        
        return Response(data)

@api_view(['POST'])
def logout_view(request):
    if request.method == 'POST':
        request.user.auth_token.delete()
        return Response("Logged Out")


@api_view(['GET','PUT','DELETE'])
@permission_classes([IsAuthenticated])
def user_settings(request,pk):
    if request.method == 'GET':
        user = User_Details.objects.get(pk=pk)
        serializer = UserSerialzer(user)
        return Response(serializer.data)

    if request.method == 'PUT':
        user = User_Details.objects.get(pk=pk)
        serializer = UserSerialzer(instance=user,data=request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
    if request.method == 'DELETE':
        user = User_Details.objects.get(pk=pk)
        user.delete()
        return Response('Deleted')

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_property(request):
    if request.method == 'POST':
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET'])
def get_property(request,arg):
    if request.method == 'GET':
        queryset= Property.objects.get(id=arg)
        serializer = PropertySerializer(queryset)
        return Response(serializer.data)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_property_image(request):
    if request.method == 'POST':
        serializer = PropertyImagesSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET'])
def get_property_images(request,arg):
    if request.method == 'GET':
        queryset= Property_Images.objects.filter(property_id=arg)
        serializer = PropertyImagesSerializer(queryset,many = True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_room(request):
    if request.method == 'POST':
        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)


@api_view(['GET'])
def get_room(request,arg):
    if request.method == 'GET':
        room= Room.objects.get(property_id=arg)
        serializer = RoomSerializer(room)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_location(request):
    if request.method == 'POST':
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

@api_view(['GET'])
def get_location(request,arg):
    if request.method == 'GET':
        location = Location.objects.get(property_id=arg)
        serializer = LocationSerializer(location)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def app_rating(request):
    if request.method == 'POST':
        serializer = AppRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
@api_view(['GET'])
def get_app_rating(request):   
    if request.method == 'GET':
        review = App_rating.objects.all()
        serializer = AppRatingSerializer(review, many = True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def property_rating(request):
    if request.method == 'POST':
        serializer = PropertyRatingSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    
@api_view(['GET'])
def get_property_rating(request):   
    if request.method == 'GET':
        review = Property_rating.objects.all()
        serializer = PropertyRatingSerializer(review, many = True)
        return Response(serializer.data)
def room_check(bed,bath,drawing_dining,balcony):
    room_given = True
    if bed is None or bath is None or drawing_dining is None or balcony is None:
        room_given = False
        return room_given
    else :
        return room_given


@api_view(['POST'])
def filter_property(request):
    if request.method == 'POST':
        serializer = FilterSerializer(data=request.data)
        if serializer.is_valid():
            filter_object = serializer.data
            room_status = room_check(filter_object['bedroom_no'],filter_object['bathroom_no'],filter_object['drawing_dining_no'],filter_object['balcony_no'])
            if room_status is True:
                if filter_object['area_sqft'] is not None and filter_object['rental_type'] is not None and filter_object['home_type'] is not None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(home_type = filter_object['home_type']).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['area_sqft'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(home_type = filter_object['home_type'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['rental_type'] is None and filter_object['home_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max']))                  
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)

                elif filter_object['rental_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(home_type = filter_object['home_type']).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['home_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    room = Room.objects.filter(property_id__in=ids).filter(bedroom_no = filter_object['bedroom_no']).filter(bathroom_no = filter_object['bathroom_no']).filter(drawing_dining_no = filter_object['drawing_dining_no']).filter(balcony_no = filter_object['balcony_no'])
                    properties = Property.objects.filter(pk__in = room).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
            else :
                if filter_object['area_sqft'] is not None and filter_object['rental_type'] is not None and filter_object['home_type'] is not None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(home_type = filter_object['home_type']).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['area_sqft'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(home_type = filter_object['home_type'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['rental_type'] is None and filter_object['home_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max']))                  
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)

                elif filter_object['rental_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(home_type = filter_object['home_type']).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
                elif filter_object['home_type'] is None:
                    queryset = Location.objects.filter(district__iexact = filter_object['district']).values('property')
                    ids = [x['property'] for x in queryset]
                    properties = Property.objects.filter(pk__in = ids).filter(rented = False)
                    searched_properties = properties.filter(rent__range = (filter_object['rent_min'],filter_object['rent_max'])).filter(Q(rental_type = filter_object['rental_type'])|Q(rental_type = 'AN')).filter(area_sqft__gte = filter_object['area_sqft'])                    
                    property_return = PropertySerializer(searched_properties,many=True)
                    return Response(property_return.data)
        else:
            return Response(serializer.errors)



@api_view(['GET'])
def location_search(request,search_topic):
    if request.method == 'GET':
        area_match = Location.objects.filter(Q(area__iexact = search_topic ) | Q(upazila__iexact = search_topic) | Q(district__iexact = search_topic) )
        properties = Property.objects.filter(pk__in = area_match).filter(rented = False)
        serializer = PropertySerializer(properties,many = True)
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def request_booking(request):
    if request.method == 'POST':
        serializer = RequestedBookingSerializer(data=request.data)
        if serializer.is_valid():
            with transaction.atomic():
                booking_instance = serializer.save()
                owner_id = Property.objects.filter(pk = serializer.data['property']).values_list('owner',flat= True)
                Received_Booking.objects.create(owner = owner_id,
                                            property = booking_instance.property,
                                            requested_user= booking_instance.user,
                                            agreement_type = booking_instance.agreement_type,
                                            start_date = booking_instance.start_date,
                                            end_date = booking_instance.end_date
                                            )
                return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_get_booking(request,user_id):
    if request.method == 'GET':
        booking_requests = Requested_Booking.objects.filter(user=user_id)
        serializer = RequestedBookingSerializer(booking_requests,many=True)
        return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def owner_get_booking(request,owner_id):
    if request.method == 'GET':
        booking_requests = Received_Booking.objects.filter(owner=owner_id)
        serializer = ReceivedBookingSerializer(booking_requests,many=True)
        return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_booking(request,arg):
    if request.method == 'POST':
        booking_requests = Received_Booking.objects.get(id = arg)
        x= booking_requests.property
        property_id_update= x.pk
        req_user = booking_requests.requested_user
        req__property =  booking_requests.property   
        with transaction.atomic():
            Rented_Property.objects.create(
                property = booking_requests.property,
                user = booking_requests.requested_user,
                agreement_type = booking_requests.agreement_type,
                start_date = booking_requests.start_date,
                end_date = booking_requests.end_date
            )
            instance = Requested_Booking.objects.filter(user = req_user).filter(property = req__property)
            instance.delete()
            Property.objects.filter(id = property_id_update).update(rented = True)
            Received_Booking.objects.get(id = arg).delete()
            

        return Response({'response':'Booking Confirmed'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_received_booking(request,arg):
    if request.method == 'DELETE':
        booking_requests = Received_Booking.objects.get(id = arg)   
        with transaction.atomic():
            instance = Requested_Booking.objects.filter(user = booking_requests.requested_user).filter(property =booking_requests.property)
            instance.delete()
            Received_Booking.objects.get(id = arg).delete()
        return Response({'response':'Booking Rejected'})

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def reject_requested_booking(request,arg):
    if request.method == 'DELETE':
        Requested_Booking.objects.get(id = arg).delete()
        return Response({'response':'Booking Canceled'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_current_home(request,user_id):
    if request.method == 'GET':
        queryset = Rented_Property.objects.filter(user=user_id).values('property')
        ids = [x['property'] for x in queryset]
        current_homes = Property.objects.filter(pk__in= ids)
        serializer = PropertySerializer(current_homes, many=True)
        return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def owners_added_propertys(request,user_id):
    if request.method == 'GET':
        queryset = Property.objects.filter(owner=user_id)
        serializer = PropertySerializer(queryset,many=True)
        return Response(serializer.data)


@api_view(['POST','DELETE'])
@permission_classes([IsAuthenticated])
def add_delete_wishlist(request):
    if request.method == 'POST':
        serializer = WishlistSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors)

    if request.method == 'DELETE':
        serializer = WishlistSerializer(data = request.data)
        if serializer.is_valid():
            Wishlist.objects.filter(user = serializer.data['user']).filter(property = serializer.data['property']).delete()
            return Response({'response':'Wishlist Removed'})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_wishlist(request,user_id):
    if request.method == 'GET':
        queryset = Wishlist.objects.filter(user = user_id).values('property')
        ids = [x['property'] for x in queryset]
        wishlist_homes = Property.objects.filter(pk__in= ids)
        serializer = PropertySerializer(wishlist_homes, many=True)
        return Response(serializer.data)
