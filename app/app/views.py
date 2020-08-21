from rest_framework import generics
from rest_framework.response import Response
from .permissions import IsOwnerOrAdminUser
from .serializers import UserProfileDetailSerializer
from auth.models import User


class UserProfileDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileDetailSerializer
    lookup_field = 'pk'
    permission_classes = (IsOwnerOrAdminUser, )

    def get(self, request, *args, **kwargs):
        up = self.get_object().profile
        serializer = self.get_serializer(up)
        return Response(serializer.data)
