from django.urls import path, include

from rest_framework import routers

from advertisement import views as ads_view
from siteapp import views as site_view

router = routers.DefaultRouter()

router.register('advertisement', ads_view.AdvertisementAPIView)
router.register('city', ads_view.CityAPIView)
router.register('statistic', ads_view.ViewStatisticAPIView)
router.register('category', ads_view.CategoryAPIView)
router.register('child-category', ads_view.ChildCategoryAPIView, 'child_category')
router.register('subscriber', ads_view.AdsSubscriberAPIView)
router.register('number', ads_view.NumberAPIView)
router.register('image', ads_view.AdsImageAPIView)

router.register('site', site_view.SiteAPIView)
router.register('social-media', site_view.SocialMediaAPIView, 'social_media')
router.register('feedback', site_view.FeedBackAPIView)
router.register('help', site_view.HelpAPIView)

urlpatterns = [
    path('', include(router.urls))
]
