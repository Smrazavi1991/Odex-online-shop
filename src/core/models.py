from django.db import models
from .fields import JDateTimeField


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField('Is Deleted', default=False, null=False, blank=False)
    last_change = JDateTimeField('Last Change', auto_now=True)
    create_date = JDateTimeField('Create Date', auto_created=True)
    delete_datetime = JDateTimeField('Delete Datetime', default=None, null=True, blank=True)
