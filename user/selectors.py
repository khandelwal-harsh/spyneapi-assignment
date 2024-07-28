from django.db.models import QuerySet
from user.models import User

def get_users() -> QuerySet[User]:
    return User.objects.all()