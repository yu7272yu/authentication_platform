from django.db import models

from user_manage.models.base_model import BaseModel
from system_manage.models.notice_info_model import NoticeInfoModel
from user_manage.models.user_info_model import UserInfoModel


class UserInfoNoticeInfoModel(BaseModel):
    browse_status = models.IntegerField(verbose_name='浏览状态')
    sh_user_info = models.ForeignKey(to=UserInfoModel, on_delete=models.PROTECT, verbose_name='用户id')
    sh_notice_info = models.ForeignKey(to=NoticeInfoModel, on_delete=models.PROTECT, verbose_name='通知信息id')

    class Meta:
        db_table = 'sh_user_info_sh_notice_info'
