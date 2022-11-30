# coding=utf-8
from django.db import models

from user_manage.models.base_model import BaseModel


class UserInfoNodeInfoModel(BaseModel):
    sh_user_role = models.ForeignKey(to='user_manage.UserRoleModel', on_delete=models.PROTECT, verbose_name='角色id')
    sh_user_info = models.ForeignKey(to='user_manage.UserInfoModel', on_delete=models.PROTECT, verbose_name='用户id')
    sh_node_info = models.ForeignKey(to='product_manage.NodeInfoModel', on_delete=models.PROTECT, verbose_name='节点id')

    class Meta:
        db_table = 'sh_user_info_sh_node_info'
