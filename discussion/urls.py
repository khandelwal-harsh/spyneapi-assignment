from django.urls import path
from discussion.apis import DiscussionCreateApi, DiscussionUpdateApi,DiscussionDeleteApi, TagListApi,DiscussionList

urlpatterns = [
    path("create/",DiscussionCreateApi.as_view(),name="create_discussion"),
    path("<int:discussion_id>/update/",DiscussionUpdateApi.as_view(),name="update_discussion"),
    path("<int:discussion_id>/delete/",DiscussionDeleteApi.as_view(),name="delete_discussion"),
    path("discussion-list/",DiscussionList.as_view(),name="list_discussion"),
    path("tag-list/",TagListApi.as_view(),name="tag_list"),
    ]