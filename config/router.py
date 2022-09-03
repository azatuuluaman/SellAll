from django.urls import path, include

from rest_framework import routers

from advertisement.views import (
    AdvertisementAPIView,
    CategoryAPIView,
    ViewStatisticAPIView,
    CityAPIView,
    ChildCategoryAPIView,
    AdsSubscriberAPIView,
)
from siteapp.views import (
    SiteAPIView,
    SocialMediaAPIView,
    FeedBackAPIView,
    HelpAPIView
)
from user.views import RegisterUserView, ActivationView

router = routers.DefaultRouter()

router.register('advertisement', AdvertisementAPIView)

urlpatterns = [
    path('', include(router.urls)),
]

urlpatterns_auth = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('activation/<str:code>/', ActivationView.as_view(), name='activate'),
]

urlpatterns_ads = [
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('child-categories/', ChildCategoryAPIView.as_view(), name='child_categories'),
    path('cities/', CityAPIView.as_view(), name='cities'),
    path('statistic/<int:pk>/', ViewStatisticAPIView.as_view(), name='statistic'),
    path('subscribers/', AdsSubscriberAPIView.as_view(), name='subscribers'),
]

urlpatterns_siteapp = [
    path('site', SiteAPIView.as_view(), name='site'),
    path('social-media', SocialMediaAPIView.as_view(), name='social_media'),
    path('feedback', FeedBackAPIView.as_view(), name='feedback'),
    path('help', HelpAPIView.as_view(), name='help'),
]

urlpatterns += urlpatterns_auth
urlpatterns += urlpatterns_ads
urlpatterns += urlpatterns_siteapp
