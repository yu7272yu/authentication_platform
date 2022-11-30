from django.db import models

from user_manage.models.base_model import BaseModel


class EnterpriseInfoModel(BaseModel):
    enterprise_name = models.CharField(max_length=32, verbose_name='企业名称', unique=True)
    enterprise_logo = models.CharField(max_length=256, verbose_name='企业logo', blank=True)
    phone_number = models.CharField(max_length=16, verbose_name='企业联系电话', blank=True)
    address = models.TextField(verbose_name='企业地址', blank=True)
    description = models.TextField(verbose_name='企业描述', blank=True)
    mark = models.TextField(verbose_name='备注信息', blank=True)

    class Meta:
        db_table = 'sh_enterprise_info'
