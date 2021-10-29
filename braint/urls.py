from django.urls import path

from braint.views import checkout_page

urlpatterns = [
    path('', checkout_page, name='checkout_page')
]