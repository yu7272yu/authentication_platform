# coding=utf-8
from django.db import models

# from app_manage.models.base_model import BaseModel
from user_manage.models.base_model import BaseModel


class UserRoleModel(BaseModel):
    role_name = models.CharField(max_length=32, verbose_name='角色名称')
    description = models.TextField(blank=True, verbose_name='角色名称')

    class Meta:
        db_table = 'sh_user_role'
