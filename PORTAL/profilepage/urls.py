from django.urls import path
from .views import ProfileView, upgrade_me, SubscriptionView, cancel_subscription, delete_account

urlpatterns = [
    path('', ProfileView.as_view(), name = 'profile'),
    path('upgrade/', upgrade_me, name = 'upgrade'),
    path('subscription/', SubscriptionView.as_view(), name='subscription'),
    path('cancel-subscription/', cancel_subscription, name='cancel_subscription'),
    path('delete-account/', delete_account, name='delete_account')
]
