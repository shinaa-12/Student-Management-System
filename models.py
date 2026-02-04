from django.db import models
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator


# Create your models here.
class Student(models.Model):
    s_id=models.AutoField(primary_key=True)
    first_name=models.CharField(max_length=100)
    last_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True, blank=True, null=True)
    phone=models.CharField( max_length=15,blank=True,validators=[RegexValidator(r'^\+?\d{7,15}$',message="Enter a valid phone number. ")])

    def __str__(self):
        return self.first_name + " - " + self.phone




    

    

   

