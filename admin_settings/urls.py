from django.urls import path
from .views import *

urlpatterns = [
    path('push/', Pushtime.as_view(), name='pushtime'),

]