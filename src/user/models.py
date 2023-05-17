from django.contrib.auth.models import AbstractUser
from core.models import BaseModel
from django.db import models


# Create your models here.
class User(AbstractUser):
    pass
    #phone
    #birthday
    #gender
    #profile_pic
    #phone_verified
    #address
    #is_staff = none

class Address(BaseModel):
    pass
    #province
    #city
    #address
    #postal code
