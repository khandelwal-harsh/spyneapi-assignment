from django.db import models
from phonenumber_field import modelfields

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    phone = modelfields.PhoneNumberField(unique=True)

    REQUIRED_FIELDS = []
    USERNAME_FIELD = "email"
    
    @property
    def is_anonymous(self):
        return True


    @property
    def is_authenticated(self):
        return True

    def get_username(self):
        return self.email

    class Meta:
        db_table = 'users'