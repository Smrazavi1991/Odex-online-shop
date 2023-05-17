from django.db import models


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    #is_deleted
    #last_change
    #create_date
    #delete_datetime