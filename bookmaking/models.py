from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import pymysql
pymysql.install_as_MySQLdb()


class User1(models.Model):
    user = models.OneToOneField(User, related_name='users', on_delete=models.CASCADE, primary_key=True)
    name = models.CharField(max_length=50, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    avatar = models.ImageField(null=True, blank=True)
    contacts = models.CharField(max_length=50, null=True, blank=True)
    bank_account = models.CharField(max_length=50, null=True, blank=True)


class Jockey(models.Model):
    jockey_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    ratio = models.FloatField()
    contacts = models.CharField(max_length=50)
    review = models.TextField()


class Horse(models.Model):
    horse_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    info = models.TextField(blank=True)
    pic = models.ImageField(null=True, blank=True)
    ratio = models.FloatField()
    jockey=models.ForeignKey(Jockey, on_delete=models.CASCADE, blank=True, null=True)
    user=models.ManyToManyField(User1, blank=True, null=True)

    def __str__(self):
        return self.name


class Ride(models.Model):
    ride_id = models.IntegerField(primary_key=True)
    date = models.DateField()
    horse = models.ManyToManyField(Horse, blank=True, null=True)


class Stake(models.Model):
    stake_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, blank=True, null=True)
    horse = models.ForeignKey(Horse, blank=True, null=True)
    size = models.FloatField(null=False, blank=False)



