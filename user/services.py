from user.helpers import model_update
from user.models import User
from user.entities import UserDataServiceEntity




class UserService:
    def create(self, data: UserDataServiceEntity) -> int:
        user_obj = User()
        user_obj.name = data.name
        user_obj.email = data.email
        user_obj.password = data.password
        user_obj.phone = data.phone

        user_obj.full_clean()
        user_obj.save()
        return user_obj.pk
    
    def update(self,data:UserDataServiceEntity, user_id: int) -> int:
        user_obj = User.objects.get(pk=user_id)
        model_update(instance=user_obj, fields=['name', 'email', 'phone'], data=data)
        return user_obj.pk
    
    def delete(self, user_id: int) -> None:
        User.objects.filter(id=user_id).delete()