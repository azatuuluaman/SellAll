from django.urls import path

from .views import (
    CategoryAPIView,
    ViewStatisticAPIView,
    CityAPIView,
    ChildCategoryAPIView,
    AdsSubscriberAPIView,
    AdsCommentCreateView,
    AdsCommentRUDView,
    CategoryRetrieveAPIView
)

urlpatterns = [
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='category'),
    path('child-categories/', ChildCategoryAPIView.as_view(), name='child_categories'),
    path('cities/', CityAPIView.as_view(), name='cities'),
    path('statistic/<int:pk>/', ViewStatisticAPIView.as_view(), name='statistic'),
    path('subscribers/', AdsSubscriberAPIView.as_view(), name='subscribers'),
    path('comment/', AdsCommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', AdsCommentRUDView.as_view(), name='comment_rud')
]