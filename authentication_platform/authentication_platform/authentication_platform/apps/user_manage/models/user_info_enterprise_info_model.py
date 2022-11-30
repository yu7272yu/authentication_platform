from django.db import models

from enterprise_manage.models.enterprise_info_model import EnterpriseInfoModel
from user_manage.models.base_model import BaseModel
from user_manage.models.user_info_model import UserInfoModel


class UserInfoEnterpriseInfoModel(BaseModel):
    show_flag = models.IntegerField(verbose_name='显示表示')
    sh_user_info = models.ForeignKey(to=UserInfoModel, on_delete=models.PROTECT, verbose_name='用户id')
    sh_enterprise_info = models.ForeignKey(to=EnterpriseInfoModel, on_delete=models.PROTECT, verbose_name='企业id')

    class Meta:
        db_table = 'sh_user_info_sh_enterprise_info'
