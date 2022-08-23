from rest_framework import viewsets

from .serializers import SiteSerializer, SocialMediaSerializer, FeedBackSerializer, HelpSerializer
from .models import Site, SocialMedia, FeedBack, Help


class SiteAPIView(viewsets.ModelViewSet):
    serializer_class = SiteSerializer
    queryset = Site.objects.all()


class SocialMediaAPIView(viewsets.ModelViewSet):
    serializer_class = SocialMediaSerializer
    queryset = SocialMedia.objects.all()


class FeedBackAPIView(viewsets.ModelViewSet):
    serializer_class = FeedBackSerializer
    queryset = FeedBack.objects.all()


class HelpAPIView(viewsets.ModelViewSet):
    serializer_class = HelpSerializer
    queryset = Help.objects.all()
