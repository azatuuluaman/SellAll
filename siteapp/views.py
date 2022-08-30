from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import SiteSerializer, SocialMediaSerializer, FeedBackSerializer, HelpSerializer
from .models import Site, SocialMedia, FeedBack, Help


class SiteAPIView(generics.ListAPIView):
    serializer_class = SiteSerializer
    queryset = Site.objects.all()
    permission_classes = (AllowAny,)


class SocialMediaAPIView(generics.ListAPIView):
    serializer_class = SocialMediaSerializer
    queryset = SocialMedia.objects.all()
    permission_classes = (AllowAny,)


class FeedBackAPIView(generics.ListAPIView):
    serializer_class = FeedBackSerializer
    queryset = FeedBack.objects.all()
    permission_classes = (AllowAny,)


class HelpAPIView(generics.ListAPIView):
    serializer_class = HelpSerializer
    queryset = Help.objects.all()
    permission_classes = (AllowAny,)
