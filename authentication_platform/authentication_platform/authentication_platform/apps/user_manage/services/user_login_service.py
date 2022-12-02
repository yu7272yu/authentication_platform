# coding=utf-8
# from app_manage.models.sh_user_info_sh_alarm_info import ShUserInfoShAlarmInfo
from authentication_platform.settings import SECRET_KEY
from authentication_platform.common.constants import Constants
from authentication_platform.common.sha256_encryption import ShaEncryption
from authentication_platform.common.jwt_token import JwtToken
from authentication_platform.common.time_helper import TimeHelper
from product_manage.models import NodeInfoModel
from user_manage.models import UserInfoNodeInfoModel
from user_manage.models.user_info_model import UserInfoModel
from authentication_platform.common.logger import Logger


class UserLoginService(object):
    def __init__(self):
        self.sha_encryption = ShaEncryption()
        self.jwt_token = JwtToken()
        self.time_helper = TimeHelper()

    def user_login_service(self, user_info_obj):
        # 校验密码--获取当前用户的对象信息
        query_dict = {
            'account__contains': user_info_obj.account,
            'account': user_info_obj.account,
            'data_status': Constants.DATA_IS_USED
        }

        try:
            user_obj = UserInfoModel.objects.filter(**query_dict).first()
        except Exception as e:
            Logger().error('user_login_service-get:{}'.format(e), Constants.USER_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        # 用户名错误--
        if user_obj is None:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PASSWORD_ERROR_MSG}

        # 密码校验
        user_password = user_obj.password
        # 加密用户传递密码作对比
        origin_password = self.sha_encryption.add_sha256(user_info_obj.password, SECRET_KEY)

        if user_password != origin_password:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PASSWORD_ERROR_MSG}

        # 通过 node_number 找到唯一的 NodeInfoModel
        node_dict = {
            'node_number': user_info_obj.node_number,
            'data_status': Constants.DATA_IS_USED,
        }
        node_info = NodeInfoModel.objects.filter(**node_dict).first()
        if not node_info:
            return {'code': Constants.DATA_IS_USED, 'msg': '该节点不存在'}
        # 通过 node_number sh_user_info_id
        user_node_dict = {
            'sh_user_info_id': user_obj.id,
            'sh_node_info': node_info.id,
            'data_status': Constants.DATA_IS_USED
        }
        user_node_info = UserInfoNodeInfoModel.objects.filter(**user_node_dict).first()
        role_info = user_node_info.sh_user_role

        # todo token 生成基础数据 account create_time
        user_info_dict = {
            'account': user_obj.account,
            'node_number': user_obj.node_number,
            'role_name': role_info.role_name,
            'create_time': self.time_helper.get_today()
        }

        user_info_dict = {
            'token': self.jwt_token.create_jwt_token(user_info_dict),
            'id': user_obj.id,
            'user_name': user_obj.user_name,
            'account': user_obj.account,
            'sh_user_role_id': role_info.id,
            'role_name': role_info.role_name,
            'phone_number': user_obj.phone_number,
            'email': user_obj.email,
            'avatar_link': user_obj.avatar_link,
            'create_time': self.time_helper.time_int_to_date(user_obj.create_time),
            'update_time': self.time_helper.time_int_to_date(user_obj.update_time),
        }

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.LOGIN_SUCCESS, 'data': user_info_dict}
