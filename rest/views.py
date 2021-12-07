from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404, CreateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet

from instagram.models import UserObject
from instagram.tasks.tasks import add_data_about_user
from rest.serializers import ListUserObjectSerializer, DetailUserObjectSerializer, ListUserObjectMediaSerializer, \
    ListUserObjectStorySerializer, CreateUserObjectSerializer


class UserObjectViewSet(ReadOnlyModelViewSet, CreateAPIView, DestroyAPIView):
    queryset = UserObject.objects.all()

    def get_serializer_class(self):
        if self.action == 'list':
            return ListUserObjectSerializer
        elif self.action == 'retrieve':
            return DetailUserObjectSerializer
        elif self.action == 'create':
            return CreateUserObjectSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        username = request.data.get('username')
        add_data_about_user.delay(username)

        return Response({
            'status': 200,
            'data': response.data
        })


    @action(methods=['GET'], detail=True, url_path='medias')
    def get_user_object_medias(self, request, *args, **kwargs) -> Response:
        """
        Возвращает все медиа пользователя
        """
        model = self.get_queryset()
        user_object = get_object_or_404(model, pk=kwargs.get('pk'))

        return Response(ListUserObjectMediaSerializer(user_object, context={"request": self.request}).data)

    @action(methods=['GET'], detail=True, url_path='stories')
    def get_user_object_stories(self, request, *args, **kwargs) -> Response:
        """
        Возвращает все истории пользователя
        """
        model = self.get_queryset()
        user_object = get_object_or_404(model, pk=kwargs.get('pk'))

        return Response(ListUserObjectStorySerializer(user_object, context={"request": self.request}).data)

    @action(methods=['GET'], detail=True, url_path='activate')
    def active_user_object(self, request, *args, **kwargs) -> Response:
        """
        Указывает, что аккаунт необходимо брать для обновления
        """
        model = self.get_queryset()
        user_object = get_object_or_404(model, pk=kwargs.get('pk'))

        user_object.activate = True
        user_object.save()

        return Response(status=202)

    @action(methods=['GET'], detail=True, url_path='deactivate')
    def deactivate_user_object(self, request, *args, **kwargs) -> Response:
        """
        Указывает, что аккаунт не надо брать для обновления
        """
        model = self.get_queryset()
        user_object = get_object_or_404(model, pk=kwargs.get('pk'))

        user_object.activate = False
        user_object.save()

        return Response(status=202)

