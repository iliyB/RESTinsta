from rest_framework import serializers

from instagram.models import UserObject


class CreateUserObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObject
        fields = ('username',)


class ListUserObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObject
        fields = ('id', 'username', 'activate',
                  'full_name', 'media_count',
                  'follower_count', 'following_count',
                  'instagram_link', 'pic', 'last_update',
                  'is_business', 'is_updated')


class DetailUserObjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObject
        exclude = ()


class ListUserObjectMediaSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObject
        fields = ('pk', 'username', 'activate',
                  'full_name', 'media_count',
                  'follower_count', 'following_count',
                  'instagram_link', 'pic', 'last_update',
                  'is_updated', 'medias')


class ListUserObjectStorySerializer(serializers.ModelSerializer):
    class Meta:
        model = UserObject
        fields = ('pk', 'username', 'activate',
                  'full_name', 'media_count',
                  'follower_count', 'following_count',
                  'instagram_link', 'pic', 'last_update',
                  'is_updated', 'stories')
