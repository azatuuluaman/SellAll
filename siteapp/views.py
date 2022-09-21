from rest_framework import generics
from rest_framework.permissions import AllowAny, IsAdminUser

from .serializers import (
    SiteSerializer,
    SocialMediaSerializer,
    FeedBackSerializer,
    HelpSerializer,
    HelpCategorySerializer,
)

from .models import (
    Site,
    SocialMedia,
    FeedBack,
    Help,
    HelpCategory
)


class SiteAPIView(generics.ListAPIView):
    serializer_class = SiteSerializer
    queryset = Site.objects.all()
    permission_classes = [AllowAny]


class SocialMediaAPIView(generics.ListAPIView):
    serializer_class = SocialMediaSerializer
    queryset = SocialMedia.objects.all()
    permission_classes = [AllowAny]


class FeedBackAPIView(generics.CreateAPIView):
    serializer_class = FeedBackSerializer
    queryset = FeedBack.objects.all()
    permission_classes = [AllowAny]


class HelpAPIView(generics.RetrieveAPIView):
    serializer_class = HelpSerializer
    queryset = Help.objects.all()
    permission_classes = [AllowAny]


class HelpCategoryAPIView(generics.ListAPIView):
    serializer_class = HelpCategorySerializer
    queryset = HelpCategory.objects.all()
    permission_classes = [AllowAny]



class FeedBackAdminView(generics.ListAPIView):
    serializer_class = FeedBackSerializer
    queryset = FeedBack.objects.all()
    permission_classes = [IsAdminUser]