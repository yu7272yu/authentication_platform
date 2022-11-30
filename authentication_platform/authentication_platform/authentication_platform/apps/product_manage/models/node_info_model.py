from django.db import models

from user_manage.models.base_model import BaseModel


class NodeInfoModel(BaseModel):
    node_name = models.CharField(max_length=32, verbose_name='节点名称')
    node_number = models.IntegerField(verbose_name='唯一标识', unique=True)
    token = models.TextField(verbose_name='token信息')
    node_method = models.IntegerField(verbose_name='启动方式')
    node_status = models.IntegerField(verbose_name='节点状态')
    service_host = models.CharField(max_length=32, verbose_name='服务ip')
    service_port = models.CharField(max_length=16, verbose_name='服务端口号')
    start_time = models.IntegerField(verbose_name='开始时间')
    end_time = models.IntegerField(verbose_name='结束时间')
    description = models.TextField(verbose_name='功能描述', blank=True)
    mark = models.TextField(verbose_name='备注信息', blank=True)
    sh_product_version = models.ForeignKey(to='product_manage.ProductVersionModel', on_delete=models.PROTECT, verbose_name='产品版本id')
    sh_enterprise_info = models.ForeignKey(to='enterprise_manage.EnterpriseInfoModel', on_delete=models.PROTECT, verbose_name='企业信息id')

    class Meta:
        db_table = 'sh_node_info'
