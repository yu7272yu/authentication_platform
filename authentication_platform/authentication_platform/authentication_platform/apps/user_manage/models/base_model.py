# coding=utf-8
import time
from django.db import models

from authentication_platform.common.constants import Constants


class BaseModel(models.Model):
    id = models.AutoField(primary_key=True, verbose_name='主键id')
    create_time = models.IntegerField(default=int(time.time()))
    update_time = models.IntegerField(default=int(time.time()), verbose_name='最后更新时间')
    data_status = models.IntegerField(default=Constants.DATA_IS_USED, verbose_name='数据状态')

    class Meta:
        abstract = True
