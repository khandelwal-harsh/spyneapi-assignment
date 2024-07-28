from django.urls import path
from user.apis import UserCreateApi,UserUpdateApi, UserDeleteApi, UserListApi

urlpatterns = [
    path("create/", UserCreateApi.as_view(), name="create_user"),
    path("list/", UserListApi.as_view(), name="create_list"),
    path("<int:user_id>/update", UserUpdateApi.as_view(), name="create_update"),
    path("<int:user_id>/delete", UserDeleteApi.as_view(), name="create_delete"),
    ]