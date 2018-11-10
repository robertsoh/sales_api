from rest_framework.generics import CreateAPIView
from apps.users.api_v1.serializers import UserSerializer


class UsersCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer
