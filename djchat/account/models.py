from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,username, email, password=None, **extra_fields):
        if not email or not username:
            raise ValueError("Email and Username are required!!")
        user = self.model(email =self.normalize_email(email), username= username, **extra_fields)
        user.set_password(password )
        user.save(using=self._db)
        return user
    
    def create_superuser(self,username, email,password):
        user = self.create_user(username, email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using = self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = "username"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS =["email"]
    objects = UserManager()
   
    def __str__(self):
       return self.username
   