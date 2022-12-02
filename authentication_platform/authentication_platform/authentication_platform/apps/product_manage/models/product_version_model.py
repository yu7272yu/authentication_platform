from django.db import models


from user_manage.models.base_model import BaseModel


class ProductVersionModel(BaseModel):
    product_version = models.CharField(max_length=32, verbose_name='产品版本')
    release_time = models.IntegerField(verbose_name='版本发布时间')
    description = models.TextField(verbose_name='版本描述', blank=True)
    mark = models.TextField(verbose_name='备注信息', blank=True)
    sh_product_info = models.ForeignKey(to='product_manage.ProductInfoModel', on_delete=models.PROTECT, verbose_name='产品id')

    class Meta:
        db_table = 'sh_product_version'
