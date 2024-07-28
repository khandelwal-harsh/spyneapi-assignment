from common.apis import BaseApi, BaseOpenApi
from user.selectors import get_users
from user.serializers import UserInputSerializer, UserModelSerializer, UserUpdateSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from user.services import UserService
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework import serializers

class UserCreateApi(BaseOpenApi):
    input_serializer_class = UserInputSerializer

    @swagger_auto_schema(
        request_body=UserInputSerializer,
        operation_id="create_user",
        responses={201: "User created successfully"},
            )
    def post(self, request, *args, **kwargs):
        data = self.validate_input_data()
        user_service = UserService()
        user_service.create(data=data)
        return Response(status=HTTP_201_CREATED)


class UserUpdateApi(BaseApi):
    input_serializer_class = UserUpdateSerializer

    @swagger_auto_schema(
        request_body=UserUpdateSerializer,
        operation_id="update_user",
        responses={200: "User updated successfully"},
    )
    def put(self, request, user_id,*args, **kwargs):
        data = self.validate_input_data()
        user_service = UserService()
        user_service.update(data=data, user_id=user_id)
        return Response(status=HTTP_200_OK)


class UserDeleteApi(BaseApi):
    @swagger_auto_schema(
        operation_id="delete_user",
        responses={200: "User deleted successfully"},
    )
    def delete(self, request, user_id,*args, **kwargs):
        user_service = UserService()
        user_service.delete(user_id=user_id)
        return Response(status=HTTP_200_OK)
    
class UserListApi(BaseApi,ListModelMixin):
    class UserSerializer(UserModelSerializer):
        class Meta(UserModelSerializer.Meta):
            fields = ("id", "name", "email", "phone")
    

    class FilterSerializer(serializers.Serializer):
        search_text = serializers.CharField(required=False)

        class Meta:
            ref_name = "UserFilterSerializer"
    
    filter_serializer_class = FilterSerializer

    def get_queryset(self):
        data = self.validate_filter_data()
        queryset = get_users()
        if data.get("search_text"):
            queryset = queryset.filter(name__icontains=data.get("search_text"))
        return queryset
        
    
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_id="list_users",
        query_serializer=FilterSerializer,
        responses={HTTP_200_OK: UserSerializer(many=True)},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

        