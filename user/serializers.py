from rest_framework import serializers

from common.serializers import BaseDataclassSerializer
from user.entities import UserDataServiceEntity, UserUpdateDataServiceEntity
from phonenumber_field import serializerfields

from user.models import User

class UserInputSerializer(BaseDataclassSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)
    phone = serializerfields.PhoneNumberField()

    class Meta:
        dataclass = UserDataServiceEntity
        ref_name = "UserInputSerializer"


class UserUpdateSerializer(BaseDataclassSerializer):
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    phone = serializerfields.PhoneNumberField()

    class Meta:
        dataclass = UserUpdateDataServiceEntity
        ref_name = "UserUpdateInputSerializer"

class UserModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"