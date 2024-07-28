from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated


from common.exceptions import SerializerMissingError


class BaseApi(GenericAPIView):
    filter_data = "query_params"
    filter_serializer_class = None
    permission_classes = [IsAuthenticated]

    input_serializer_class = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.validated_data = None

    def get_input_context(self):
        return self.get_serializer_context()

    def get_filter_context(self):
        return {}


    def validate_data(self, serializer_class, data, context={}):
        serializer = serializer_class(data=data, context=context)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def validate_filter_data(self, copy=True):
        if not self.filter_serializer_class:
            raise SerializerMissingError("Filter serializer missing.")
        if copy:
            data = self.request.query_params.copy() if self.filter_data == "query_params" else self.request.data.copy()
        else:
            data = self.request.query_params if self.filter_data == "query_params" else self.request.data
        return self.validate_data(self.filter_serializer_class, data, context=self.get_filter_context())

    def validate_input_data(self, copy=True):
        if not self.input_serializer_class:
            raise SerializerMissingError("Input serializer missing.")
        if copy:
            data = self.request.data.copy()
        else:
            data = self.request.data

        self.validated_data = self.validate_data(self.input_serializer_class, data, context=self.get_input_context())
        return self.validated_data

    def get_paginated_data(self):
        is_paginated = False
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            is_paginated = True
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data), is_paginated
        serializer = self.get_serializer(queryset, many=True)
        return serializer.data, is_paginated
    
class BaseOpenApi(BaseApi):
    permission_classes = (AllowAny,)