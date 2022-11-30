from django.db import models


from user_manage.models.base_model import BaseModel


class ProductVersionModel(BaseModel):
    product_version = models.CharField(max_length=32, verbose_name='产品版本')
    mirror_link = models.CharField(max_length=128, verbose_name='镜像链接')
    git_url = models.CharField(max_length=128, verbose_name='git地址')
    commit_id = models.CharField(max_length=128, verbose_name='CommitID')
    release_time = models.IntegerField(verbose_name='版本发布时间')
    description = models.TextField(verbose_name='版本描述', blank=True)
    mark = models.TextField(verbose_name='备注信息', blank=True)
    sh_product_info = models.ForeignKey(to='product_manage.ProductInfoModel', on_delete=models.PROTECT, verbose_name='产品id')
    sh_function_info = models.ManyToManyField(to='product_manage.FunctionInfoModel')

    class Meta:
        db_table = 'sh_product_version'
