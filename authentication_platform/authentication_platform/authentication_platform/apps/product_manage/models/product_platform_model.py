from django.db import models


from user_manage.models.base_model import BaseModel


class ProductPlatformModel(BaseModel):
    product_platform = models.CharField(max_length=32, verbose_name='产品平台')
    mirror_link = models.CharField(max_length=128, verbose_name='镜像链接')
    git_url = models.CharField(max_length=128, verbose_name='git地址')
    commit_id = models.CharField(max_length=128, verbose_name='CommitID')
    description = models.TextField(verbose_name='平台描述', blank=True)
    mark = models.TextField(verbose_name='备注信息', blank=True)
    sh_product_version = models.ForeignKey(to='product_manage.ProductVersionModel', on_delete=models.PROTECT, verbose_name='产品版本id')
    sh_function_info = models.ManyToManyField(to='product_manage.FunctionInfoModel')

    class Meta:
        db_table = 'sh_product_version'
