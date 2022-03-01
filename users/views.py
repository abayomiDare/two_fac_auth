from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from .serializers import *
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

User = get_user_model()


@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
@api_view(['GET', 'POST'])
def user(request):
    if request.method == 'GET':

        obj = User.objects.all()
        serializer = UserSerializer(obj, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
            user = User.objects.create(**serializer.validated_data)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def get_userid(request, user_id):
    try:
        user = User.objects.get(user_id)
    except User.DoesNotExist:
        return Response({"message": "user does not exist"}, status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PUT':
        serializer = UserSerializer(User, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response({"message": "successfully deleted"}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication, SessionAuthentication])
@permission_classes([IsAuthenticated])
def base_view(request):
    if request.method == 'GET':
        content = {'message': 'Hello, World!'}
        return Response(content)
