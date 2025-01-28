from django.urls import path
from .views import *

urlpatterns = [
    path('', ProfileView.as_view(), name = 'profile'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
]
