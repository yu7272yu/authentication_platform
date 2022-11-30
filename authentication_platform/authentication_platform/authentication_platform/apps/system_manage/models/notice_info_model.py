from django.db import models

from product_manage.models.node_info_model import NodeInfoModel
from user_manage.models.base_model import BaseModel
from user_manage.models.user_info_model import UserInfoModel


class NoticeInfoModel(BaseModel):
    notice_title = models.TextField(verbose_name='通知标题')
    notice_info = models.TextField(verbose_name='通知详情')
    notice_type = models.IntegerField(verbose_name='消息种类')
    sh_user_info = models.ForeignKey(to=UserInfoModel, on_delete=models.PROTECT, verbose_name='创建人id')
    sh_node_info = models.ForeignKey(to=NodeInfoModel, on_delete=models.PROTECT, verbose_name='消息来源id')

    class Meta:
        db_table = 'sh_notice_info'
