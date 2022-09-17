from django.urls import path

from advertisement.views.favorite_views import FavoriteAPIView
from advertisement.views.other_views import (
    CategoryAPIView,
    CityAPIView,
    ChildCategoryAPIView,
    CategoryRetrieveAPIView,
)

from advertisement.views.advertisement_views import (
    AdvertisementCreateView,
    AdvertisementListView,
    AdvertisementRUDView,
    SimularAdsView,
    ComplainingForAdsView,
    UserAdvertisementListView,
)

from advertisement.views.comment_views import AdsCommentCreateView, AdsCommentRUDView
from advertisement.views.statistic_views import AddPhoneView, StatisticsView

urlpatterns = [
    path('create/', AdvertisementCreateView.as_view(), name='ads_create'),
    path('list/', AdvertisementListView.as_view(), name='ads_list'),
    path('users-ads/', UserAdvertisementListView.as_view(), name='users_ads'),
    path('<int:pk>/', AdvertisementRUDView.as_view(), name='ads'),
    path('categories/', CategoryAPIView.as_view(), name='categories'),
    path('category/<int:pk>/', CategoryRetrieveAPIView.as_view(), name='category'),
    path('child-categories/', ChildCategoryAPIView.as_view(), name='child_categories'),
    path('cities/', CityAPIView.as_view(), name='cities'),
    path('statistic/<int:pk>/', StatisticsView.as_view(), name='statistic'),
    path('comment/', AdsCommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/', AdsCommentRUDView.as_view(), name='comment_rud'),
    path('phone_view/<int:pk>/', AddPhoneView.as_view(), name='phone_view'),
    path('simular/<int:child_category_id>/', SimularAdsView.as_view(), name='simular'),
    path('complaining/', ComplainingForAdsView.as_view(), name='complaining'),
    path('favorites/', FavoriteAPIView.as_view(), name='favorites'),
]
