from django.db import models

from user_manage.models.base_model import BaseModel


class ProductInfoModel(BaseModel):
    product_name = models.CharField(max_length=32, verbose_name='产品名称')
    description = models.TextField(verbose_name='产品描述', blank=True)
    mark = models.TextField(verbose_name='备注信息', blank=True)

    class Meta:
        db_table = 'sh_product_info'
