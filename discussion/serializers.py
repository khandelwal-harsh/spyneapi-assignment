from common.serializers import BaseSerializer, BaseDataclassSerializer
from rest_framework import serializers

from discussion.entities import DiscussionCreateServiceEntity, TagCreateServiceEntity


class TagCreateSerializer(BaseDataclassSerializer):
    name = serializers.CharField()
    
    class Meta:
        dataclass = TagCreateServiceEntity

class DiscussionCreateSerializer(BaseDataclassSerializer):
    description = serializers.CharField()
    image = serializers.URLField(required=False, allow_null=True, default=None)
    tags = TagCreateSerializer(many=True,required=False, allow_null=True, default=None)
    
    def validate_tags(self, attrs):
        tags = attrs
        set_tag = set()
        for tag in tags:
            if tag.name in set_tag:
                raise serializers.ValidationError("Duplicate tags are not allowed")
            set_tag.add(tag.name)
        return attrs

    class Meta:
        dataclass= DiscussionCreateServiceEntity