from django.contrib.auth.models import User
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from user_profile.permissions import IsOneself
from user_profile.serializers import UserSerializer


class ListCreateUserAPIView(APIView):
    def post(self, request: Request):
        user_sr = UserSerializer(data=request.data)

        if user_sr.is_valid(raise_exception=True):
            user_sr.save()

            user = User.objects.get(id=user_sr['id'].value)
            user.is_active = 0
            user.save()

            return Response(data=user_sr.data)

    def get(self, request: Request):
        users = User.objects.all()

        return Response(data=UserSerializer(users, many=True).data)


class RetrieveUpdateDestroyAPIView(APIView):
    permission_classes = (IsOneself,)

    def get(self, request: Request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with {user_id=} does not exist'}, status=400)

        self.check_object_permissions(request, user)

        return Response(UserSerializer(user).data)

    def patch(self, request: Request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with {user_id=} does not exist'}, status=400)

        user_sr = UserSerializer(user, data=request.data, partial=True)

        if user_sr.is_valid(raise_exception=True):
            self.check_object_permissions(request, user)
            user_sr.save()

            return Response(data=user_sr.data)

        return Response(data={'error': 'Wrong parameters'})

    def put(self, request: Request, user_id: int):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': f'User with {user_id=} does not exist'}, status=400)

        user_sr = UserSerializer(user, data=request.data)

        if user_sr.is_valid(raise_exception=True):
            self.check_object_permissions(request, user)
            user_sr.save()

            return Response(data=user_sr.data)

        return Response(data={'error': 'Wrong parameters'})
