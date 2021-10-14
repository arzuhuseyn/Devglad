from django.contrib.auth import get_user_model

from rest_framework import permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView

from catalog.models import Representative
from api.serializers import (
    RepresentativeSerializer, HumanSerializer, human_list, UserSerializer,
    UserOverViewSerializer
)


User = get_user_model()


class RepresentativeAPIView(APIView):
    serializer_class = RepresentativeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        if kwargs.get('pk'):
            obj = Representative.objects.get(pk=kwargs.get('pk'))
            serializer = self.serializer_class(obj)
        else:
            qs = Representative.objects.all()
            serializer = self.serializer_class(qs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class HumansAPIView(APIView):
    serializer_class = HumanSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(human_list, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    overview_serializer_class=UserOverViewSerializer

    def get_serializer_class(self):
        serializer = self.overview_serializer_class
        if self.request.method == 'GET':
            serializer = self.serializer_class
        return serializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserOverViewSerializer

