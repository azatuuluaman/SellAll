from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from advertisement.permissions import IsAuthorComment

from advertisement.serializers import AdsCommentSerializer

from advertisement.models import (
    AdsComment,
)


class AdsCommentCreateView(generics.CreateAPIView):
    serializer_class = AdsCommentSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super(AdsCommentCreateView, self).post(request, *args, **kwargs)


class AdsCommentRUDView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AdsCommentSerializer
    queryset = AdsComment.objects.all()
    permission_classes = [IsAuthorComment]

    def put(self, request, *args, **kwargs):
        request.data['user'] = request.user.pk
        return super(AdsCommentRUDView, self).put(request, *args, **kwargs)
