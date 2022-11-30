from django.db import models

from product_manage.models.functional_info_model import FunctionInfoModel
from product_manage.models.node_info_model import NodeInfoModel
from user_manage.models.base_model import BaseModel


class FunctionConfigureModel(BaseModel):
    limit_num = models.IntegerField(verbose_name='数量限制', default=0)
    mark = models.TextField(verbose_name='备注信息', blank=True)
    sh_function_info = models.ForeignKey(to=FunctionInfoModel, on_delete=models.PROTECT, verbose_name='产品功能id')
    sh_node_info = models.ForeignKey(to=NodeInfoModel, on_delete=models.PROTECT, verbose_name='产品节点id')

    class Meta:
        db_table = 'sh_function_configure'