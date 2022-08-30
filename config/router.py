from django.urls import path, include

from rest_framework import routers

from advertisement.views import (
    AdvertisementAPIView,
    CategoryAPIView,
    ViewStatisticAPIView,
    CityAPIView,
    ChildCategoryAPIView,
    AdsSubscriberAPIView,
    AdsImageAPIView,
    NumberAPIView,
)
from siteapp import views as site_view
from user.views import RegisterUserView, ActivationView, ForgotPasswordView

router = routers.DefaultRouter()

router.register('advertisement', AdvertisementAPIView)

router.register('site', site_view.SiteAPIView)
router.register('social-media', site_view.SocialMediaAPIView, 'social_media')
router.register('feedback', site_view.FeedBackAPIView)
router.register('help', site_view.HelpAPIView)

urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('child-categories/', ChildCategoryAPIView.as_view(), name='child_categories'),
    path('cities/', CityAPIView.as_view(), name='cities'),
    path('statistic/<int:pk>/', ViewStatisticAPIView.as_view(), name='statistic'),
    path('subscribers/', AdsSubscriberAPIView.as_view(), name='subscribers'),
    path('numbers/', NumberAPIView.as_view(), name='numbers'),
    path('images/', AdsImageAPIView.as_view(), name='images'),
    path('register/', RegisterUserView.as_view(), name='register'),
    path('activation/<str:code>/', ActivationView.as_view(), name='activate'),
    path('forgot_password/', ForgotPasswordView.as_view(), name='forgot_password'),
    path('', include(router.urls)),
]
