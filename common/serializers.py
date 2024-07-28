from rest_framework_dataclasses.serializers import DataclassSerializer
from rest_framework import serializers

class BaseDataclassSerializer(DataclassSerializer):
    pass


class BaseSerializer(serializers.Serializer):
    pass

class SplitCharListField(serializers.ListField):
    """Splits Character using comma(",")  for GET APIs"""

    def run_child_validation(self, data):
        result = []
        for _data in data:
            for idx, item in enumerate(_data.strip().split(",")):
                result.append(item)

        return result
