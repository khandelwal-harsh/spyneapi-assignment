from django.db import models
from user.models import User

class Discussion(models.Model):
    description = models.TextField()
    image = models.ImageField(upload_to="discussions/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="created_by", on_delete=models.RESTRICT)
    updated_at = models.DateTimeField(null=True, blank=True)
    updated_by = models.ForeignKey(User, related_name="updated_by", null=True, blank=True, on_delete=models.RESTRICT)
    
    
    class Meta:
        db_table = "discussions"


class Tag(models.Model):
    name = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name="tag_created_by", on_delete=models.RESTRICT)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = "tags"


class DiscussionTag(models.Model):
    discussion = models.ForeignKey(Discussion, on_delete=models.CASCADE, related_name="tags")
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name="discussions")
    
    def __str__(self):
        return f"{self.discussion.title} - {self.tag.name}"
    
    class Meta:
        db_table = "discussion_tags"