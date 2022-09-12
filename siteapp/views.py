from rest_framework import generics
from rest_framework.permissions import AllowAny

from .serializers import (
    SiteSerializer,
    SocialMediaSerializer,
    FeedBackSerializer,
    HelpSerializer,
    HelpCategorySerializer,
    # FooterSerializer
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


# class FooterAPIView(views.APIView):
#     def get(self, request):
#         categories = Category.objects.all()
#         cities = City.objects.all()
#         apps = SocialMedia.objects.filter(type=settings.APP)
#         networks = SocialMedia.objects.filter(type=settings.SOCIAL_NETWORK)
#
#         data = [
#             {
#                 'category': categories,
#                 'city': cities,
#                 'app': apps,
#                 'network': networks
#             }
#         ]
#
#         serializer = FooterSerializer(data=data, many=True)
#         serializer.is_valid(raise_exception=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
