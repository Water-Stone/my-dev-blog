from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin


class UserManager(BaseUserManager):
    def create_user(self, username, nickname, password=None):
        if not username:
            raise ValueError("username is needed")
    
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, nickname, password=None):
        user = self.create_user(
            username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        verbose_name="username",
        max_length=255,
        unique=True
    )
    
    nickname = models.CharField(
        verbose_name="nickname",
        max_length=255
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = []
    
    # def __str__(self) -> str:
    #     return f"{str(self.nickname)}({self.username})"

    # def has_perm(self, _perm, _obj=None):
    #     return True

    # def has_module_perms(self, _app_label):
    #     return True