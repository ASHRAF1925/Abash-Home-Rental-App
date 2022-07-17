from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver 
from rest_framework.authtoken.models import Token
#auto creating tokens
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
# Create your models here.
class User_Details(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key = True)
    first_name = models.CharField(blank = True,max_length=255)
    last_name = models.CharField(blank = True,max_length=255)
    profile_pic = models.ImageField(null=True, blank = True, upload_to = 'user_images/')
    email = models.EmailField(blank = True)
    phone = models.CharField(blank = True,max_length=14)
    birth_date = models.DateField(null=True, blank = True)
    nid_number = models.CharField(blank = True,max_length=10)
    nid_file = models.FileField(null= True, blank = True ,upload_to='nids/')
    def __str__(self):
        return self.first_name

class Property(models.Model):
    HOME_TYPE_CHOICES = [
        ('F','Furnished'),
        ('N','Non-Furnished')
    ]
    AGREEMENT_CHOICES = [
        ('M','Monthly'),
        ('W','Weekly'),
        ('D','Daily'),
        ('A', 'Any')
    ]
    RENTAL_TYPE_CHOICES = [
        ('FF','Family Flat'),
        ('BF','Bachelor Flat'),
        ('FS','Family Sublet'),
        ('BS','Bachelor Sublet'),
        ('AN', 'Any')
    ]
    owner = models.ForeignKey(User_Details,on_delete=models.CASCADE)
    rental_type = models.CharField(null= True,blank=True,max_length=2,choices= RENTAL_TYPE_CHOICES)
    home_type = models.CharField(null= True,blank=True,max_length=1,choices=HOME_TYPE_CHOICES)
    property_image = models.ImageField(null= True,blank=True,upload_to = 'property_images/')
    rent = models.IntegerField()
    area_sqft = models.DecimalField(null= True,blank=True,max_digits=9, decimal_places=2)
    agreement = models.CharField(max_length=1,choices=AGREEMENT_CHOICES)
    floor = models.CharField(max_length=20)
    negotiable = models.BooleanField()
    rented = models.BooleanField()

    def __str__(self):
        return str(self.pk)

class Property_Images(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    more_images = models.ImageField(null=True,blank=True,upload_to = 'more_property_images/')
    def __str__(self):
        return str(self.property)

class Room(models.Model):
    property = models.OneToOneField(Property,on_delete=models.CASCADE,primary_key = True)
    bedroom_no = models.IntegerField()
    bathroom_no = models.IntegerField()
    drawing_dining_no = models.IntegerField(null=True)
    balcony_no = models.IntegerField(null=True)
    def __str__(self):
        return str(self.property)

class Location(models.Model):
    property = models.OneToOneField(Property,on_delete=models.CASCADE,primary_key = True)
    flat = models.CharField(max_length=50)
    house = models.CharField(max_length=100)
    road = models.CharField(max_length=100)
    area = models.CharField(max_length=100)
    ward = models.IntegerField()
    upazila = models.CharField(max_length=30)
    district = models.CharField(max_length=30)
    division = models.CharField(max_length=30)
    latitude = models.CharField(null=True,max_length=100)
    longitude = models.CharField(null=True,max_length=100)
    def __str__(self):
        return str(self.property)

class Requested_Booking(models.Model):
    AGREEMENT_CHOICES = [
        ('M','Monthly'),
        ('W','Weekly'),
        ('D','Daily')
    ]
    user = models.ForeignKey(User_Details,on_delete=models.CASCADE)
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    agreement_type = models.CharField(max_length=1,choices=AGREEMENT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    rejected = models.BooleanField(null=True)
    def __str__(self):
        return str(self.user)
class Received_Booking(models.Model):
    AGREEMENT_CHOICES = [
        ('M','Monthly'),
        ('W','Weekly'),
        ('D','Daily')
    ]
    owner = models.IntegerField()
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    requested_user = models.ForeignKey(User_Details,on_delete=models.CASCADE)
    agreement_type = models.CharField(max_length=1,choices=AGREEMENT_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return str(self.owner)

class Rented_Property(models.Model):
    AGREEMENT_CHOICES = [
        ('M','Monthly'),
        ('W','Weekly'),
        ('D','Daily')
    ]
    property = models.OneToOneField(Property,on_delete=models.CASCADE, primary_key= True)
    user = models.ForeignKey(User_Details,on_delete=models.CASCADE)
    agreement_type = models.CharField(null = True,max_length=1,choices=AGREEMENT_CHOICES)
    start_date = models.DateField(null = True)
    end_date = models.DateField(null = True)

    def __str__(self):
        return str(self.property)

class Wishlist(models.Model):
    user = models.ForeignKey(User_Details,on_delete=models.CASCADE)
    property = models.ForeignKey(Property,on_delete=models.CASCADE)
    def __str__(self):
        return str(self.user)

class Property_rating(models.Model):
    user = models.ForeignKey(User_Details,on_delete=models.PROTECT)
    property = models.ForeignKey(Property,on_delete=models.PROTECT)
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    review = models.TextField()
    def __str__(self):
        return str(self.property)

class App_rating(models.Model):
    user = models.ForeignKey(User_Details,on_delete=models.PROTECT)
    rating = models.DecimalField(max_digits=2,decimal_places=1)
    review = models.TextField(max_length = 255)
    def __str__(self):
        return str(self.user)
