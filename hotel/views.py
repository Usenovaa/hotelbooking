from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Room, Hotel, Booking, Rating, Comment
from .serializers import HotelSerializer, BookingSerializer, RoomSerializer, RatingSerializer, CommentSerializer
from rest_framework import permissions
from django_filters import rest_framework as filters
from rest_framework import filters as rest_filters
from .permissions import IsAuthorOrReadOnly, IsAdminPermission
from likes.mixins import LikedMixin

class HotelViewset(viewsets.ModelViewSet, LikedMixin):
    queryset = Hotel.objects.all()
    serializer_class = HotelSerializer
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter
    ]
    filterset_fields = ['name', 'location']
    search_fields = ['name']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'delete':
            return HotelSerializer
        elif self.action == 'retrieve':
            return HotelSerializer
        return HotelSerializer

    @action(['GET'], detail=True)
    def comments(self, request, pk=None):
        hotel = self.get_object()
        comment = hotel.comments.all()
        serializer = CommentSerializer(
            comment, many=True
        ).data
        return Response(serializer, status=200)


class RoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    filter_backends = [
        filters.DjangoFilterBackend,
        rest_filters.SearchFilter
    ]
    filterset_fields = ['room_num', 'price']
    search_fields = ['hotel']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAdminUser()]
        return [permissions.IsAuthenticatedOrReadOnly()]

    def get_serializer_class(self):
        if self.action == 'list' or self.action == 'delete':
            return RoomSerializer
        elif self.action == 'retrieve':
            return RoomSerializer
        return RoomSerializer


class BookingViewset(viewsets.ModelViewSet):
    queryset = Booking.objects.all()
    serializer_class = BookingSerializer
    # permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class CommentListViewset(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_context(self):
        return {
            'request': self.request
        }

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)


class RatingVieset(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]

    def get_serializer_context(self):
        return {'request': self.request}

    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)
