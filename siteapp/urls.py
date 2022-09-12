from django.urls import path

from .views import (
    SiteAPIView,
    SocialMediaAPIView,
    FeedBackAPIView,
    HelpAPIView,
    HelpCategoryAPIView,
)

urlpatterns = [
    path('site/', SiteAPIView.as_view(), name='site'),
    path('social-media/', SocialMediaAPIView.as_view(), name='social_media'),
    path('feedback/', FeedBackAPIView.as_view(), name='feedback'),
    path('help-category/', HelpCategoryAPIView.as_view(), name='help_category'),
    path('help/<int:pk>/', HelpAPIView.as_view(), name='help'),
    # path('footer/', FooterAPIView.as_view(), name='footer')
]
