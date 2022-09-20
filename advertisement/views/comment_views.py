from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

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

    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        sql = f"""with recursive tree (id, text, advertisement_id, parent_id, user_id)
                as (select id, text, advertisement_id, parent_id, user_id from advertisement_adscomment
                where parent_id is null and advertisement_id = {id}
            union all
               select ads.id, ads.text, ads.advertisement_id,
                      ads.parent_id, ads.user_id from advertisement_adscomment as ads
                 inner join tree on tree.id = ads.parent_id)
            select id, text, advertisement_id, parent_id, user_id from tree"""
        queryset = AdsComment.objects.raw(sql)
        serializer = AdsCommentSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

