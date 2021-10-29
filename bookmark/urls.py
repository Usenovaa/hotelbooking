from django.urls import path

from bookmark.views import (
    BookmarkListAPIView,
    BookmarkCreateAPIView,
    BookmarkDeleteAPIView,
)


urlpatterns = [
    path('list/', BookmarkListAPIView.as_view(), name='list'),
    path('create/', BookmarkCreateAPIView.as_view(), name='create'),
    path('delete/<int:pk>/', BookmarkDeleteAPIView.as_view(), name='delete'),
]
