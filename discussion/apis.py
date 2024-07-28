from common.apis import BaseApi, BaseOpenApi
from common.serializers import SplitCharListField
from discussion.models import Discussion, DiscussionTag, Tag
from discussion.serializers import DiscussionCreateSerializer
from discussion.services import DiscussionService
from drf_yasg.utils import swagger_auto_schema
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response
from rest_framework.mixins import ListModelMixin
from rest_framework import serializers
from django.db import transaction

class DiscussionCreateApi(BaseOpenApi):
    input_serializer_class = DiscussionCreateSerializer


    @swagger_auto_schema(
        request_body=DiscussionCreateSerializer,
        operation_id="create_discussion",
        responses={HTTP_201_CREATED: "Discussion created successfully"},
    )
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        data = self.validate_input_data()
        discussion_service = DiscussionService()
        discussion_service.create(data=data, user_id=request.user.pk)
        return Response(status=HTTP_201_CREATED)


class DiscussionUpdateApi(BaseApi):
    input_serializer_class = DiscussionCreateSerializer

    @swagger_auto_schema(
        request_body=DiscussionCreateSerializer,
        operation_id="update_discussion",
        responses={HTTP_200_OK: "Discussion updated successfully"},
    )
    @transaction.atomic
    def put(self, request, discussion_id, *args, **kwargs):
        data = self.validate_input_data()
        discussion_service = DiscussionService()
        discussion_service.update(data=data, discussion_id=discussion_id, user_id=request.user.pk)
        return Response(status=HTTP_200_OK)


class DiscussionDeleteApi(BaseApi):
    @swagger_auto_schema(
        operation_id="delete_discussion",
        responses={HTTP_200_OK: "Discussion deleted successfully"},
    )
    @transaction.atomic
    def delete(self, request, discussion_id, *args, **kwargs):
        discussion_service = DiscussionService()
        discussion_service.delete(discussion_id=discussion_id, user_id=request.user.pk)
        return Response(status=HTTP_200_OK)


class TagListApi(BaseApi):
    class TagSerializer(serializers.ModelSerializer):
        class Meta:
            fields = ("id", "name")
            model = Tag

    @swagger_auto_schema(
        operation_id="list_tags",
        responses={HTTP_200_OK: TagSerializer},
    )
    def get(self, request, *args, **kwargs):
        tags = Tag.objects.all()
        serializer = self.TagSerializer(tags, many=True)
        return Response(serializer.data)


class DiscussionList(BaseApi, ListModelMixin):
    class DiscussionSerializer(serializers.ModelSerializer):
        tags = serializers.SerializerMethodField()

        def get_tags(self, obj):
            return [{"id":tag.tag_id,"name":tag.tag.name} for tag in obj.tags.all()]

        class Meta:
            fields = ("id", "description", "image", "created_by", "tags")
            model = Discussion

    class FilterSerializer(serializers.Serializer):
        search_text = serializers.CharField(required=False)
        tags = SplitCharListField(required=False)

        class Meta:
            ref_name = "DiscussionFilterSerializer"


    def get_queryset(self):
        data = self.validate_filter_data()
        queryset = Discussion.objects.prefetch_related("tags").all()
        if data.get("search_text"):
            queryset = queryset.filter(description__icontains=data.get("search_text"))
        if data.get("tags"):
            queryset = DiscussionTag.objects.filter(tag_id__in=data.get("tags")).values_list("discussion_id", flat=True)
            queryset = Discussion.objects.filter(id__in=queryset)
        return queryset
            

    serializer_class = DiscussionSerializer
    filter_serializer_class = FilterSerializer

    @swagger_auto_schema(
        operation_id="list_discussion",
        query_serializer=FilterSerializer,
        responses={HTTP_200_OK: DiscussionSerializer},
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

