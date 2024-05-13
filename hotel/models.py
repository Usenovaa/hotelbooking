from datetime import datetime, date, timedelta
from django.contrib.contenttypes.fields import GenericRelation
from django.db import models
from django.contrib.auth import get_user_model
from likes.models import Like

User = get_user_model()


class Hotel(models.Model):
    name = models.CharField(max_length=20)
    location = models.CharField(max_length=50)
    phone = models.CharField(max_length=20)
    image = models.ImageField(upload_to='images', default='default.png', null=True, blank=True)
    likes = GenericRelation(Like)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save()

    @property
    def total_likes(self):
        return self.likes.count()


class Room(models.Model):
    room_num = models.IntegerField()
    price = models.IntegerField()
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='rooms')
    is_booked = models.BooleanField(default=False)

    class Meta:
        ordering = ['id']


class Booking(models.Model):
    author = models.ForeignKey(User, related_name='bookings', on_delete=models.CASCADE, null=True)
    hotel = models.ForeignKey(Hotel, related_name='bookings', on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='bookings', on_delete=models.CASCADE)
    num_of_guest = models.IntegerField(default=1)
    checkin_date = models.DateField()
    checkout_date = models.DateField()
    is_checkout = models.BooleanField(default=False)

    def __str__(self):
        return "self.id"

    def hotel_name(self):
        return self.hotel

    def pay(self):
        return (self.checkout_date - self.checkin_date + timedelta(1)).days*self.room.price


class Rating(models.Model):
    author = models.ForeignKey(User, related_name='ratings', on_delete=models.CASCADE, null=True)
    rating = models.IntegerField()
    hotel = models.ForeignKey(Hotel, related_name='ratings', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.rating} - {self.hotel}'


class Comment(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    author = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE, null=True)
    hotel = models.ForeignKey(Hotel, related_name='comments', on_delete=models.CASCADE)

    class Meta:
        ordering = ['created']

