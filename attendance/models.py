from django.db import models
from django.utils import timezone


class Person(models.Model):

    PART_CHOICES = (
        ('S', '소프라노'),
        ('A', '알토'),
        ('T', '테너'),
        ('B', '베이스'),
    )

    name = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    birth = models.CharField(max_length=10)
    birth_monthday = models.CharField(max_length=4, default='')
    part = models.CharField(max_length=1, choices=PART_CHOICES)
    is_active = models.BooleanField(default=True)
    create_dt = models.DateTimeField(default=timezone.now)


class Song(models.Model):
    no = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=40)
    author = models.CharField(max_length=60)
    play_time = models.CharField(max_length=20)


class Practice(models.Model):
    song = models.ForeignKey(Song)
    practice_dt = models.DateField()
    create_dt = models.DateTimeField(default=timezone.now)


class Attendance(models.Model):
    person = models.ForeignKey(Person)
    practice = models.ForeignKey(Practice)
    is_join = models.BooleanField(default=False)




