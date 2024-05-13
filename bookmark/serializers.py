from rest_framework import serializers

from hotel.models import Hotel
from bookmark.models import Bookmark
from hotel.serializers import HotelSerializer


class BookmarkListSerializer(serializers.ModelSerializer):

    hotel = HotelSerializer()

    class Meta:
        model = Bookmark
        fields = ['hotel']


class BookmarkCreateSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    # def validate_post(self, post):
    #     user = self.context['request'].user
    #     if (
    #         not post.user.private
    #         or post.user == user
    #         or post.id
    #         in Post.objects.filter(
    #             user_id__in=user.following.values_list('id', flat=True)
    #         ).values_list('id', flat=True)
    #     ):
    #         return post
    #     else:
    #         raise serializers.ValidationError('Not allowed!')

    class Meta:
        model = Bookmark
        fields = '__all__'
