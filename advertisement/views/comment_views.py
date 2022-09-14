from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from advertisement.permissions import IsAuthorComment

from advertisement.serializers import (
    AdsCommentSerializer,
)

from advertisement.models import (
    AdsComment,
)


class AdsCommentCreateView(generics.CreateAPIView):
    serializer_class = AdsCommentSerializer
    permission_classes = [IsAuthenticated]


class AdsCommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdsCommentSerializer
    queryset = AdsComment.objects.all()
    permission_classes = [IsAuthorComment]
