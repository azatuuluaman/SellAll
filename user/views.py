from django.shortcuts import render

# Create your views here.
# class UserList(generics.ListCreateAPIView):
#     permission_classes = (IsAuthenticatedOrWriteOnly,)
#     serializer_class = UserSerializer
#
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)