import pymysql,sys, os, django
import re
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'authentication_platform.settings')
django.setup()

from app_manage.models.app_info_model import AppInfoModel
from user_manage.models.user_info_model import UserInfoModel
from user_manage.models.user_role_model import UserRoleModel
from app_manage.models.app_info_model import AppInfoModel
from resource_manage.models.manufacturer_info_model import ManufacturerInfoModel
from resource_manage.models.machine_type_model import MachineTypeModel
from plan_manage.models.weekly_schedule_model import WeeklyScheduleModel
from threshold_manage.models.threshold_type_model import ThresholdTypeModel
from resource_manage.models.electronic_map_model import ElectronicMapModel

from authentication_platform.common.sha256_encryption import ShaEncryption
from authentication_platform.common.constants import Constants
from authentication_platform.settings import Config, SECRET_KEY


def mysql_db():
    print('开始创建数据库')
    db = pymysql.connect(
        host=  Config.mysql_host,  # 连接名称，默认127.0.0.1
        user= Config.mysql_user,  # 用户名
        passwd= Config.mysql_password ,  # 密码
        port= Config.mysql_port ,  # 端口，默认为3306
        charset='utf8mb4',  # 字符编码
    )
    cursor = db.cursor() #创建游标对象

    try:
        sql = 'show databases' 
        cursor.execute(sql)
        print('未创建数据库前：',cursor.fetchall()) #获取创建数据库前全部数据库

        dbname = Config.mysql_db
        sql = 'create database if not exists %s'%(dbname) #创建数据库
        cursor.execute(sql)

        sql = 'show databases' 
        cursor.execute(sql)
        print('创建新的数据库后：',cursor.fetchall()) #获取创建数据库后全部数据库
        # sql = 'drop database if exists %s'%(dbname) #删除数据库
        # cursor.execute(sql)
    except Exception as e:
        print('创建数据库失败：', e)
        db.rollback()  #回滚事务

    finally:
        cursor.close() 
        db.close()  #关闭数据库连接

def migrate_db():
    try:
        os.system('python3 authentication_platform/manage.py makemigrations user_manage app_manage auth_code_manage threshold_manage resource_manage  plan_manage' )
        os.system('python3 authentication_platform/manage.py migrate' )
        db = pymysql.connect(
            host=  Config.mysql_host,  # 连接名称，默认127.0.0.1
            user= Config.mysql_user,  # 用户名
            passwd= Config.mysql_password ,  # 密码
            port= Config.mysql_port ,  # 端口，默认为3306
            charset='utf8mb4',  # 字符编码
            database=Config.mysql_db     #指定操作的数据库
        )
        cursor = db.cursor() #创建游标对象
        sql = 'show tables'
        cursor.execute(sql)
        tables = [cursor.fetchall()]
        table_ll = re.findall('(\'.*?\')', str(tables))
        table_list = [re.sub("'", '', each) for each in table_ll]
        print('显示创建的表:', table_list)  #显示创建的表

    except Exception as e:
        print('创建数据表异常:', e)  #显示创建的表
        db.rollback()  #回滚事务
    finally:
        cursor.close() 
        db.close()


def initial_data():
    try:
        print("开始创建数据")
        # 应用
        for i, val in enumerate( Config.app_name_list):
            t, res = AppInfoModel.objects.get_or_create(app_name=val, data_status=Constants.DATA_IS_USED)
            if res :
                t.sorted_num= i+1
                t.save()

        # 角色
        r1, r1_res = UserRoleModel.objects.get_or_create(role_name="超级管理员", data_status=Constants.DATA_IS_USED )
        r2, r2_res = UserRoleModel.objects.get_or_create(role_name="管理员", data_status=Constants.DATA_IS_USED )
        r2, r2_res = UserRoleModel.objects.get_or_create(role_name="普通用户", data_status=Constants.DATA_IS_USED )

        # 用户
        u_1={'user_name': 'root','sh_user_role_id': r1.id, 'data_status': Constants.DATA_IS_USED }
        user_1, u1_res = UserInfoModel.objects.get_or_create(**u_1)
        if u1_res:
            user_1.user_password = ShaEncryption().add_sha256('123456', SECRET_KEY)
            user_1.save()

        user_1.app_info.add(*AppInfoModel.objects.all())

        # 厂家
        for i, val in enumerate( Config.manufacturer_name_list):
            t, res = ManufacturerInfoModel.objects.get_or_create(manufacturer_name=val, data_status=Constants.DATA_IS_USED)
        
        # 设备类型
        for i, val in enumerate( Config.machine_type_list):
            t, res = MachineTypeModel.objects.get_or_create(machine_type=val, data_status=Constants.DATA_IS_USED)

        # 阈值
        for i, val in enumerate( Config.threshold_type_list):
            tt, res = ThresholdTypeModel.objects.get_or_create(threshold_type=val, data_status=Constants.DATA_IS_USED)
            tt.app_info.clear()
            if val == '检测阈值':
                tt.app_info.add(*AppInfoModel.objects.all())
            elif val == '违停时间阈值' or val == '短信提示阈值':
                app_infos = AppInfoModel.objects.filter(app_name='违停').all()
                tt.app_info.add(*app_infos)
            elif val == '限速阈值':
                tt.app_info.add(*AppInfoModel.objects.filter(app_name='区间测速').all())
            elif val == '删除阈值':
                app_infos = AppInfoModel.objects.all()
                tt.app_info.add(*app_infos)
            elif val == '速度阈值':
                tt.app_info.add(*AppInfoModel.objects.filter(app_name='奔跑检测').all())
            elif val == '人数阈值':
                tt.app_info.add(*AppInfoModel.objects.filter(app_name='奔跑检测').all())
            elif val == '人车数量阈值':
                tt.app_info.add(*AppInfoModel.objects.filter(app_name='行进方向检测').all())
            elif val == '人车停留时间阈值':
                tt.app_info.add(*AppInfoModel.objects.filter(app_name='行进方向检测').all())
            elif val == '单位时间阈值':
                tt.app_info.add(*AppInfoModel.objects.filter(app_name='行进方向检测').all())
            elif val == '变化量阈值':
                tt.app_info.add(*AppInfoModel.objects.filter(app_name='行进方向检测').all())

        # 日期
        week_values = [['周一',0],['周二',1],['周三',2],['周四',3],['周五',4],['周六',5],['周日',6]]
        for i, val in enumerate( week_values ):
            WeeklyScheduleModel.objects.get_or_create(weekly_day=val[0], weekly_id=val[1])
        print("数据创建成功")

        el = ElectronicMapModel.objects.first()
        if not el:
            ElectronicMapModel.objects.create(**{'center_longitude': 0, 'center_latitude': 0, 'minimum_level': 16, 'sh_user_info_id': r1.id })

    except Exception as e:
        print("创建数据失败:", e)
        
        
if __name__ == '__main__':
    mysql_db()
    migrate_db()
    initial_data()
