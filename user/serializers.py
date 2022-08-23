# from rest_framework import serializers
# from .models import User
#
#
# # class UserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = ('id', 'email', 'first_name', 'last_name', 'phone')
#
# class ProfileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = ('first_name', 'last_name', 'gender', 'zip_code',)
#
#
# class UserSerializer(serializers.ModelSerializer):
#     profile = ProfileSerializer(required=True)
#
#     class Meta:
#         model = User
#         fields = ('url', 'email', 'profile', 'created',)
#
#     def create(self, validated_data):
#         # create user
#         user = User.objects.create(
#             url=validated_data['url'],
#             email=validated_data['email'],
#             # etc ...
#         )
#
#         profile_data = validated_data.pop('profile')
#         # create profile
#         profile = Profile.objects.create(
#             user=user
#         first_name = profile_data['first_name'],
#                      last_name = profile_data['last_name'],
#         # etc...
#         )
#
#         return user
