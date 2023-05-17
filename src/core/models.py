from django.db import models


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField('Is Deleted', default=False, null=False, blank=False)
    last_change = models.DateTimeField(auto_now=True)
    create_date = models.DateTimeField(auto_created=True)
    delete_datetime = models.DateTimeField(default=None, null=True, blank=True)
