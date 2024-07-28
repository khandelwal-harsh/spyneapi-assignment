from dj_rest_auth.serializers import TokenSerializer
from django.db import transaction
from rest_framework import serializers, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response

from user.models import User
from common.apis import BaseOpenApi
from common.serializers import BaseSerializer
from spyneai.jwt import encode
from drf_yasg.utils import swagger_auto_schema


class LoginAuthTokenApi(BaseOpenApi):
    class InputSerializer(BaseSerializer):
        password = serializers.CharField()
        email = serializers.EmailField()

        class Meta:
            ref_name = "ValidateInputToken"
            input_hash_id_fields = ()

    input_serializer_class = InputSerializer
    serializer_class = InputSerializer

    class OutputSerializer(BaseSerializer):
        token = serializers.CharField()

        class Meta:
            ref_name = "ValidateOutputToken"
            output_hash_id_fields = ()

    @swagger_auto_schema(
        operation_id="login_auth",
        request_body=InputSerializer,
        responses={status.HTTP_201_CREATED: OutputSerializer()},
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = self.validate_input_data()
        user = User.objects.filter(email=data["email"], password=data["password"]).first()
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND, data={"message": "User not found"})
        token, _ = Token.objects.get_or_create(user=user)
        serializer = TokenSerializer(instance=token).data
        return Response({"token": encode(serializer)}, status=status.HTTP_201_CREATED)
