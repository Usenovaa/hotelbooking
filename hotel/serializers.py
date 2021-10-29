from django.db.models import Avg
from psycopg2._range import DateTimeRange
from rest_framework import serializers
from .models import Hotel, Room, Booking, Rating, Comment
import pandas
from likes import services as likes_services


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ['id', 'name', 'location', 'phone', 'image', ]

    def to_representation(self, instance):
        representation = super(HotelSerializer, self).to_representation(instance)
        request = self.context.get('request')
        representation['comments'] = CommentSerializer(
            Comment.objects.filter(hotel=instance.id),
            many=True
        ).data
        representation['likes_count'] = instance.likes.count()
        r = instance.ratings.aggregate(Avg('rating'))
        representation['ratings'] = r['rating__avg']

        return representation


class RoomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Room
        fields = ['room_num', 'price', 'hotel', 'is_booked', 'id']


class BookingSerializer(serializers.ModelSerializer):
    # hotel = HotelSerializer
    # room = RoomSerializer

    def validate(self, attrs):
        chin_date = attrs.get('checkin_date')
        room_ = attrs.get('room')
        obj = Booking.objects.values()
        for room in obj:
            dates = pandas.date_range(room.get('checkin_date'), room.get('checkout_date'))
            d = []
            for i in dates:
                d.append(i)
            if room.get('room_id') == room_.id and chin_date in d:
                raise ValueError(
                    'Занято!'
                )
        return attrs

    class Meta:
        model = Booking
        fields = ['id', 'author', 'hotel', 'room', 'num_of_guest', 'checkin_date', 'checkout_date', 'pay']

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        booking = Booking.objects.create(author=author, **validated_data)
        return booking


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        comment = Comment.objects.create(author=author, **validated_data)
        return comment


class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ['id', 'rating', 'author', 'hotel']

    def create(self, validated_data):
        request = self.context.get('request')
        author = request.user
        rating = Rating.objects.create(author=author, **validated_data)
        return rating

    def validate_hotel(self, hotel):
        if self.Meta.model.objects.filter(hotel=hotel).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на данный продукт'
            )
        return hotel

    def validate_rating(self, rating):
        if rating not in range(1, 6):
            raise serializers.ValidationError(
                'Рейтипг должен быть от 1 до 5'
            )
        return rating

