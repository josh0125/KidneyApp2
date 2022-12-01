from django.db import models

# Create your models here.
from datetime import datetime


class Person(models.Model):
    personid = models.BigAutoField(primary_key=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=2)
    zip = models.CharField(max_length=10)
    phone = models.CharField(max_length=14)
    email = models.CharField(max_length=100)
    username = models.CharField(max_length=50, default=None, blank=True, null=True)
    password = models.CharField(max_length=50, default=None, blank=True, null=True)
    gender = models.CharField(max_length=10, default=None, blank=True, null=True)
    race = models.CharField(max_length=50, default=None, blank=True, null=True)
    age = models.IntegerField(default=0)
    height = models.IntegerField(default=0)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    morbidities = models.ManyToManyField('Morbidity')

    def __str__(self):
        return (self.first_name + ' ' + self.last_name)


class Morbidity(models.Model):
    morbidityid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    datediagnosed = models.DateField(blank=True)

    def __str__(self):
        return (self.name)


class LabVitals(models.Model):
    vitalid = models.BigAutoField(primary_key=True)
    personid = models.ForeignKey(
        Person, null=True, blank=True, on_delete=models.SET_NULL)
    K = models.DecimalField(max_digits=5, decimal_places=2)
    Phos = models.DecimalField(max_digits=5, decimal_places=2)
    Na = models.DecimalField(max_digits=5, decimal_places=2)
    Creatinine = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    Albumin = models.DecimalField(max_digits=5, decimal_places=2)
    BloodSugar = models.IntegerField(default=0)
    BloodPressure = models.CharField(max_length=10)
    Weight = models.DecimalField(max_digits=5, decimal_places=2)
    Date = models.DateField(blank=True)

    def __str__(self):
        return (str(self.vitalid))


class Food(models.Model):
    foodid = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=50)
    
    sodium = models.DecimalField(max_digits=5, decimal_places=2)
    protein = models.DecimalField(max_digits=5, decimal_places=2)
    k = models.DecimalField(max_digits=5, decimal_places=2)
    phosphorus = models.DecimalField(max_digits=5, decimal_places=2)
    sugar = models.IntegerField(default=0)
    cholesterol = models.DecimalField(max_digits=5, decimal_places=2)
    water = models.IntegerField(default=0)
    

    def __str__(self):
        return (self.name)


class FoodEntry(models.Model):
    foodentryid = models.BigAutoField(primary_key=True)
    date = models.DateField(blank=True)
    mealType = models.CharField(max_length=20)
    personid = models.ForeignKey(
        Person, null=True, blank=True, on_delete=models.SET_NULL)
    foods = models.ManyToManyField('Food')

    def __str__(self):
        return (self.mealType)

class JournalEntry(models.Model):
    entryid = models.BigAutoField(primary_key=True)
    personid = models.ForeignKey(
        Person, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=True)
    notes = models.CharField(max_length=3000)
    status = models.CharField(max_length=25)

    def __str__(self):
        return (self.status)


class ExerciseEntry(models.Model):
    exerciseid = models.BigAutoField(primary_key=True)
    personid = models.ForeignKey(
        Person, null=True, blank=True, on_delete=models.SET_NULL)
    date = models.DateField(blank=True)
    duration = models.IntegerField(default=0)
    weight = models.IntegerField(default=0)

    def __str__(self):
        return (str(self.duration))
