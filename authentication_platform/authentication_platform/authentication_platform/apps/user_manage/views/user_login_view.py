# coding=utf-8
import random
import string

import cv2
from django.http import StreamingHttpResponse

from authentication_platform.common.base_view import BaseView
from django_redis import get_redis_connection
from authentication_platform.common.constants import Constants
from user_manage.objects.user_info_object import UserObject
from user_manage.services.user_login_service import UserLoginService


class UserLoginView(BaseView):
    def __init__(self):
        self.redis_client = get_redis_connection("default")
        self.user_login_service = UserLoginService()

    def get_user_code(self, request):
        """
        随机生成登录验证码--登录页面请求数据
        :param request:
        :return:
        """
        # 限制请求频率
        user_ip = request.META['REMOTE_ADDR']

        limit_code_flag = '{}_code'.format(user_ip)
        now_num = self.redis_client.get(limit_code_flag)

        # 有值和没有值需要分开处理
        if now_num:
            # 数据值大于了限制次数
            if int(now_num) >= Constants.LOGIN_IP_LIMIT_NUM:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.LOGIN_IP_LIMIT_MSG}
            # 在有效次数内  则新增即可
            else:
                self.redis_client.incr(limit_code_flag)
        # 当前ip没有请求标识--则直接新增且设置过期时长
        else:
            self.redis_client.incr(limit_code_flag)
            self.redis_client.expire(limit_code_flag, Constants.RANDOM_CODE_TIMEOUT)

        # 随机生成字符串
        code_str = ''.join(
            [random.choice(string.ascii_letters + string.digits) for i in range(Constants.RANDOM_CODE_NUM)])

        # 存储入redis
        self.redis_client.set(code_str.lower(), code_str, Constants.RANDOM_CODE_TIMEOUT)

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.WEB_REQUEST_MSG_OK, 'data': code_str}

    def user_login(self, request):
        account = request.POST.get('account')
        password = request.POST.get('password')
        user_code = request.POST.get('user_code')
        # node_number 节点唯一标识符
        node_number = request.POST.get('node_number')

        # todo--获取登录ip--如果1分钟内 当前ip登录超过3次 则不让登录
        user_ip = request.META['REMOTE_ADDR']

        if not all([account, password, user_code]):
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        limit_login_flag = str(user_ip)
        now_num = self.redis_client.get(limit_login_flag)

        # 有值和没有值需要分开处理
        if now_num:
            # 数据值大于了限制次数
            if int(now_num) >= Constants.LOGIN_IP_LIMIT_NUM:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.LOGIN_IP_LIMIT_MSG}
            # 在有效次数内  则新增即可
            else:
                self.redis_client.incr(limit_login_flag)
        # 当前ip没有请求标识--则直接新增且设置过期时长
        else:
            self.redis_client.incr(limit_login_flag)
            self.redis_client.expire(limit_login_flag, Constants.RANDOM_CODE_TIMEOUT)

        # 校验验证码
        redis_code = self.redis_client.get(user_code.lower())

        if not redis_code:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.RANDOM_CODE_IS_TIMEOUT}

        if redis_code.decode('utf-8').lower() != user_code.lower():
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.RANDOM_CODE_IS_ERROR}

        # 验证码 校验后 则直接删除
        self.redis_client.delete(user_code.lower())
        # 校验账号名称和密码
        user_info_obj = UserObject()
        user_info_obj.account = account
        user_info_obj.password = password
        user_info_obj.node_number = node_number

        return self.user_login_service.user_login_service(user_info_obj)