from api_app.models import Employee
from django_filters import rest_framework as filters
from django.db import connection
from django.conf import settings


def get_filter_fields_arugments(Model):
    fields = {}
    options = Model._meta

    for field in options.fields:
        try:
            db_field_type = field.rel_db_type(connection).split('(')[0]
        except :
            db_field_type = 'default'

        fields[field.name] = settings.FILTER_OPTIONS.get(db_field_type, 'default')

    return fields


class EmployeeFilter(filters.FilterSet):
    class Meta:
        model = Employee
        # fields = {
        #     "empCity": ["exact", "icontains", "istartswith"],
        #     "empName": ["exact", "icontains", "istartswith"],
        #     "empID": ["exact", 'gte', 'lte'],
        # }
        fields = get_filter_fields_arugments(model)

