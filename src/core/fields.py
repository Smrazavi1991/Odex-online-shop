from django.db import models
import jdatetime


class JDateTimeField(models.DateTimeField):
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return jdatetime.datetime.fromgregorian(datetime=value)

    def to_python(self, value):
        if isinstance(value, jdatetime.datetime):
            return value
        elif value is None:
            return value
        return jdatetime.datetime.fromgregorian(datetime=value)

    def get_prep_value(self, value):
        if isinstance(value, jdatetime.datetime):
            return value.togregorian()
        elif value is None:
            return value
        return super().get_prep_value(value)
