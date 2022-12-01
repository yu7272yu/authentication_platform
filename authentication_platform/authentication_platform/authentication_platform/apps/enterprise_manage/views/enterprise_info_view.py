# coding=utf-8
from django.http import QueryDict

from authentication_platform.common.base_view import BaseView
from authentication_platform.common.fdfs_util.fdfs_util import FastDfsUtil
from authentication_platform.common.logger import Logger
from authentication_platform.common.constants import Constants
from enterprise_manage.objects.enterprise_info_object import EnterpriseInfoObject
from enterprise_manage.services.enterprise_info_service import EnterpriseInfoService


class EnterpriseInfoView(BaseView):
    """

    """

    def __init__(self):
        self.enterprise_info_service = EnterpriseInfoService()

    def enterprise_info_list(self, request):
        """
        公司信息列表
        :param request:
        :return:
        """
        page = int(request.GET.get('page', 1))
        limit = int(request.GET.get('limit', 10))

        enterprise_name = request.POST.get('enterprise_name')

        enterprise_info_obj = EnterpriseInfoObject()
        enterprise_info_obj.enterprise_name = enterprise_name
        enterprise_info_obj.page = page
        enterprise_info_obj.limit = limit

        return self.enterprise_info_service.enterprise_info_list_service(enterprise_info_obj)

    def enterprise_info_add(self, request):
        """
        新增公司信息
        :param request:
        :return:
        """
        enterprise_name = request.POST.get('enterprise_name')
        enterprise_logo = request.FILE.get('enterprise_logo')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        mark = request.POST.get('mark')
        remote_id = None

        if not enterprise_name:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        if enterprise_logo:
            code, enterprise_logo, remote_id = FastDfsUtil().upload_by_buffer_request(request, enterprise_logo)
            if code == Constants.WEB_REQUEST_CODE_ERROR:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PIC_UPLOAD_ERROR}

        enterprise_info_obj = EnterpriseInfoObject()
        enterprise_info_obj.enterprise_name = enterprise_name
        enterprise_info_obj.enterprise_logo = enterprise_logo
        enterprise_info_obj.phone_number = phone_number
        enterprise_info_obj.address = address
        enterprise_info_obj.mark = mark

        re_json = self.enterprise_info_service.enterprise_info_add_service(enterprise_info_obj)
        if re_json['code'] == Constants.WEB_REQUEST_CODE_ERROR:
            FastDfsUtil().delete(remote_id)
        return re_json

    def enterprise_info_update(self, request):
        """
        更新公司信息
        :param request:
        :return:
        """
        sh_enterprise_info_id = request.POST.get('id')
        enterprise_name = request.POST.get('enterprise_name')
        enterprise_logo = request.FILE.get('enterprise_logo')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        mark = request.POST.get('mark')
        remote_id = None

        if not sh_enterprise_info_id:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}

        if enterprise_logo:
            code, enterprise_logo, remote_id = FastDfsUtil().upload_by_buffer_request(request, enterprise_logo)
            if code == Constants.WEB_REQUEST_CODE_ERROR:
                return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.PIC_UPLOAD_ERROR}

        enterprise_info_obj = EnterpriseInfoObject()
        enterprise_info_obj.sh_enterprise_info_id = sh_enterprise_info_id
        enterprise_info_obj.enterprise_name = enterprise_name
        enterprise_info_obj.enterprise_logo = enterprise_logo
        enterprise_info_obj.phone_number = phone_number
        enterprise_info_obj.address = address
        enterprise_info_obj.mark = mark

        re_json = self.enterprise_info_service.enterprise_info_update_service(enterprise_info_obj)
        if re_json['code'] == Constants.WEB_REQUEST_CODE_ERROR:
            FastDfsUtil().delete(remote_id)
        return re_json

    def enterprise_info_delete(self, request):
        """
        批量删除公司信息
        :param request:
        :return:
        """
        data = QueryDict(request.body)
        id_str = str(data.get('id')).split(',')

        list_enterprise_info_obj = []
        if not id_str:
            return {'code': Constants.WEB_REQUEST_CODE_ERROR, 'msg': Constants.HAVE_NO_ENOUGH_PARAMS}
        else:
            for id_one in id_str:
                enterprise_info_obj = EnterpriseInfoObject()
                enterprise_info_obj.sh_enterprise_info_id = id_one
                list_enterprise_info_obj.append(enterprise_info_obj)

        return self.enterprise_info_service.enterprise_info_delete_list_service(list_enterprise_info_obj)
