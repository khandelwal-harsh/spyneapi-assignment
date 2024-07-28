from typing import List
from common.services import model_update
from discussion.entities import DiscussionCreateServiceEntity, TagCreateServiceEntity
from discussion.models import Discussion, Tag, DiscussionTag

class DiscussionService:
    def create(self, data:DiscussionCreateServiceEntity,user_id: int):
        disc_obj = Discussion()
        disc_obj.description = data.description
        disc_obj.image = data.image
        disc_obj.created_by_id = user_id
        
        disc_obj.full_clean()
        disc_obj.save()
        if data.tags:
            self._bulk_create_discussion_tags(tags=data.tags, discussion_id=disc_obj.pk, user_id=user_id)
    
    def _bulk_create_discussion_tags(self, tags: List[TagCreateServiceEntity], discussion_id: int,user_id:int):
        already_existed_tags = Tag.objects.filter(name__in=[tag.name for tag in tags])
        mapping = {tag.name: tag for tag in already_existed_tags}
        to_create_tags = [tag for tag in tags if tag.name not in mapping]
        created_tags = Tag.objects.bulk_create([Tag(name=tag.name, created_by_id=user_id) for tag in to_create_tags])
        created_tags.extend(already_existed_tags)
        
        if created_tags:
            DiscussionTag.objects.bulk_create([DiscussionTag(discussion_id=discussion_id, tag_id=tag.pk) for tag in created_tags])

    def _bulk_delete_discussion_tags(self, discussion_id: int):
        DiscussionTag.objects.filter(discussion_id=discussion_id).delete()


    def update(self, data:DiscussionCreateServiceEntity, discussion_id:int, user_id: int):
        discussion_instance = Discussion.objects.get(pk=discussion_id)
        if discussion_instance.created_by_id != user_id:
            raise PermissionError("You are not allowed to update this discussion")
        model_update(instance=discussion_instance, data=data,fields=["description", "image"])

        if data.tags:
            self._bulk_delete_discussion_tags(discussion_id=discussion_id)
            self._bulk_create_discussion_tags(tags=data.tags, discussion_id=discussion_id, user_id=user_id)

    def delete(self, discussion_id: int, user_id: int):
        discussion_instance = Discussion.objects.get(pk=discussion_id)
        if discussion_instance.created_by_id != user_id:
            raise PermissionError("You are not allowed to update this discussion")
        discussion_instance.delete()
        self._bulk_delete_discussion_tags(discussion_id=discussion_id)
