from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from django.conf.urls import url
from rest_framework import permissions
from rest_framework.routers import DefaultRouter

from braint.views import payment
from hotel.views import HotelViewset, RoomViewset, BookingViewset, RatingVieset, CommentListViewset
from hotelbooking import settings
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

router = DefaultRouter()
router.register('hotels', HotelViewset)
router.register('rooms', RoomViewset)
router.register('bookings', BookingViewset)
router.register('ratings', RatingVieset)
router.register('comments', CommentListViewset)

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    url(r'^swagger(?P<format>.json|.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('admin/', admin.site.urls),
    path('api/h1/account/', include('account.urls')),
    path('chat/', include('chat.urls')),
    path('oplata/', include('braint.urls')),
    path('payment/', payment, name='payment'),
    path('api/h1/', include(router.urls)),
    path('api/h1/bookmark/', include('bookmark.urls')),
]

urlpatterns += static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)
