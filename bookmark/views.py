from django.db.models import QuerySet

from rest_framework.renderers import JSONRenderer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView


from bookmark.serializers import BookmarkListSerializer, BookmarkCreateSerializer


class BookmarkListAPIView(ListAPIView):

    serializer_class = BookmarkListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self) -> QuerySet:
        return self.request.user.bookmarks.all()


class BookmarkCreateAPIView(CreateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = BookmarkCreateSerializer
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer) -> None:
        serializer.save(user=self.request.user)


class BookmarkDeleteAPIView(DestroyAPIView):
    lookup_url_kwarg = 'pk'
    lookup_field = 'hotel__pk'
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return self.request.user.bookmarks.all()
