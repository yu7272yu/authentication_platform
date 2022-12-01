# coding=utf-8
import time
from django.db import transaction

from enterprise_manage.models import EnterpriseInfoModel
from user_manage.models.user_info_model import UserInfoModel
from authentication_platform.common.constants import Constants
from authentication_platform.common.logger import Logger
from authentication_platform.common.obj_to_dict import ObjToDict


class EnterpriseInfoService(object):
    def __init__(self):
        self.obj_to_dict = ObjToDict()

    def enterprise_info_list_service(self, enterprise_info_obj):
        try:
            kwargs = {'data_status': Constants.DATA_IS_USED}

            # 根据名字查找
            if enterprise_info_obj.enterprise_name:
                kwargs['enterprise_name__icontains'] = enterprise_info_obj.machine_name

            enterprise_info = EnterpriseInfoModel.objects.filter(**kwargs).order_by('-id')
        except Exception as e:
            error_msg = 'enterprise_info_list--{}({})'.format(Constants.SELECT_SQL_ERROR, e)
            Logger().error(error_msg, Constants.ENTERPRISE_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.SELECT_SQL_ERROR}

        if not enterprise_info:
            return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.HAVE_NO_EXPECT_DATA,
                    'data': Constants.DATA_DETAIL, 'num': Constants.DATA_NUM}

        start_index = (enterprise_info_obj.page - 1) * enterprise_info_obj.limit
        end_index = enterprise_info_obj.page * enterprise_info_obj.limit

        # 获取查询结果总数
        list_num = enterprise_info.count()

        return_list = []
        for one_obj in enterprise_info[start_index: end_index]:
            one_dict = {
                "id": one_obj.id,
                "enterprise_name": one_obj.enterprise_name,
                "enterprise_logo": one_obj.enterprise_logo,
                "phone_number": one_obj.phone_number,
                "address": one_obj.address,
                "description": one_obj.description,
                "mark": one_obj.mark,
            }
            return_list.append(one_dict)

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.WEB_REQUEST_MSG_OK, 'num': list_num,
                'data': return_list}

    def enterprise_info_add_service(self, enterprise_info_obj):
        """
        授权码信息不存在数据库
        :param add_auth_code_obj:
        :return:
        """
        try:
            # 查找该名称公司是否已存在
            enterprise_info_dict = {
                'enterprise_name': enterprise_info_obj.enterprise_name,
                'data_status': Constants.DATA_IS_USED,
            }
            enterprise_info = EnterpriseInfoModel.objects.filter(**enterprise_info_dict).first()
            if enterprise_info:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_ALREADY_EXISTS}

            enterprise_info_dict = self.obj_to_dict.obj_to_dict(enterprise_info_obj)
            add_enterprise_info = UserInfoModel.objects.create(**enterprise_info_dict)

        except Exception as e:
            error_msg = 'enterprise_info_add--{}({})'.format(Constants.DATA_ADD_ERROR, e)
            Logger().error(error_msg, Constants.ENTERPRISE_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_ADD_ERROR}

        return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_ADD_OK, 'data': add_enterprise_info}

    def enterprise_info_update_service(self, enterprise_info_obj):
        try:
            # 查找该名称公司是否已存在
            enterprise_info_dict = {
                'enterprise_name': enterprise_info_obj.enterprise_name,
                'data_status': Constants.DATA_IS_USED,
            }
            enterprise_info = EnterpriseInfoModel.objects.filter(**enterprise_info_dict).first()
            if enterprise_info:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_ALREADY_EXISTS}
            # 查询id 对象是否存在
            enterprise_info_dict = {
                'id': enterprise_info_obj.sh_enterprise_info_id,
                'data_status': Constants.DATA_IS_USED,
            }
            enterprise_info = EnterpriseInfoModel.objects.filter(**enterprise_info_dict).first()
            if not enterprise_info:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_IS_NOT_EXISTS}

            enterprise_info_obj.sh_machine_resource_id = None
            enterprise_info_dict = self.obj_to_dict.obj_to_dict(enterprise_info_obj)

            res = EnterpriseInfoModel.objects.filter(id=enterprise_info.id, update_time=enterprise_info.update_time).update(**enterprise_info_dict, update_time=int(time.time()))
            if res:
                return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_UPDATE_OK}
            else:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_IS_CHANGED}

        except Exception as e:
            error_msg = 'enterprise_info_update--{}({})'.format(Constants.DATA_UPDATE_ERROR, e)
            Logger().error(error_msg, Constants.ENTERPRISE_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_UPDATE_ERROR}

    @transaction.atomic
    def enterprise_info_delete_list_service(self, list_enterprise_info_obj):
        code = Constants.WEB_REQUEST_CODE_OK
        msg = Constants.DATA_DELETE_OK
        for enterprise_info_obj in list_enterprise_info_obj:
            # 创建保存点
            save_id = transaction.savepoint()
            json = self.enterprise_info_delete_service(enterprise_info_obj)
            if json['code'] == Constants.WEB_REQUEST_CODE_ERROR:
                transaction.savepoint_rollback(save_id)
                code = json['code']
                msg = json['msg']
            # 成功，提交保存点
            transaction.savepoint_commit(save_id)
        return {'code': code, 'msg': msg}

    def enterprise_info_delete_service(self, enterprise_info_obj):
        try:
            # 查询id 对象是否存在
            enterprise_info_dict = {
                'id': enterprise_info_obj.sh_enterprise_info_id,
            }
            enterprise_info = EnterpriseInfoModel.objects.filter(**enterprise_info_dict).first()
            if not enterprise_info:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_IS_NOT_EXISTS}

            res = EnterpriseInfoModel.objects.filter(id=enterprise_info.id, update_time=enterprise_info.update_time).update(data_status=Constants.DATA_IS_DELETED, update_time=int(time.time()))
            if res:
                return {'code': Constants.WEB_REQUEST_CODE_OK, 'msg': Constants.DATA_DELETE_OK}
            else:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_IS_CHANGED}

        except Exception as e:
            error_msg = 'enterprise_info_delete--{}({})'.format(Constants.DATA_DELETE_ERROR, e)
            Logger().error(error_msg, Constants.ENTERPRISE_MANAGE_LOG)
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.DATA_DELETE_ERROR}
