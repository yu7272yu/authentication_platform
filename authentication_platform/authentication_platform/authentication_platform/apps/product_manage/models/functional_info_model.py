from django.db import models

from product_manage.models.product_info_model import ProductInfoModel
from user_manage.models.base_model import BaseModel


class FunctionInfoModel(BaseModel):
    functional_module = models.CharField(max_length=32, verbose_name='产品功能或者应用')
    release_time = models.IntegerField(verbose_name='功能发布时间', blank=True)
    description = models.TextField(verbose_name='功能描述', blank=True)
    mark = models.TextField(verbose_name='备注信息', blank=True)

    class Meta:
        db_table = 'sh_product_info'
