from django.db import models


# Create your models here.
class Employee(models.Model):
    emp_name = models.CharField(max_length=100)
    emp_category = models.CharField(max_length=100, blank=True)
    emp_city = models.CharField(max_length=50)
    emp_org = models.CharField(max_length=50, blank=True)
    emp_start_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.emp_name

