from django.db import models
from django_jalali.db import models as jmodels
import jdatetime
import datetime


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField('Is Deleted', default=False, null=False, blank=False)
    last_change = jmodels.jDateTimeField('Last Change', auto_now=True, editable=False)
    create_date = jmodels.jDateTimeField('Create Date', auto_now_add=True, editable=False)
    delete_datetime = jmodels.jDateTimeField('Delete Datetime', default=None, null=True, blank=True, editable=False)

    def create_delete_datetime(self):
        if self.is_deleted is True:
            self.delete_datetime = jdatetime.datetime.fromgregorian(datetime=datetime.datetime)
