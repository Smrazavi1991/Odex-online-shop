from django.db import models
from django_jalali.db import models as jmodels
from django.utils import timezone
import jdatetime
import datetime


# Create your models here.
class BaseModel(models.Model):
    class Meta:
        abstract = True

    is_deleted = models.BooleanField('Is Deleted', default=False)
    last_change = jmodels.jDateTimeField('Last Change', auto_now=True, editable=False)
    create_date = jmodels.jDateTimeField('Create Date', auto_now_add=True, editable=False)
    delete_datetime = jmodels.jDateTimeField('Delete Datetime', default=None, null=True, blank=True, editable=False)

    # def delete(self, using=None, keep_parents=False):
    #     _ = super().delete(using, keep_parents)
    #     self.delete_datetime = timezone.now()
    #     self.save()
    #     return _
    #
    def create_delete_datetime(self):
        if self.is_deleted is True:
            self.delete_datetime = datetime.datetime.now().replace(microsecond=0)
