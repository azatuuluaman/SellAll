from rest_framework import views
from rest_framework.permissions import IsAuthenticated


class FavoriteAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        return
