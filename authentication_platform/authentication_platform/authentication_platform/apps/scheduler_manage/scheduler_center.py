# coding=utf-8
import time
import redis
import random
import datetime
from apscheduler.schedulers.background import BackgroundScheduler

from video_analysis_platform.common.kafka_util.kafka_service import KafkaUtil
from resource_manage.services.machine_resource_service import MachineResourceService
from config import Config
from video_analysis_platform.common.logger import Logger
from video_analysis_platform.apps.app_manage.services.app_info_service import AppInfoService
from video_analysis_platform.common.constants import Constants
from video_analysis_platform.apps.plan_manage.services.test_plan_service import TestPlanVersion
# from authentication_platform.apps.resource_manage.services.machine_node_service import MachineNodeService

class SchedulerCenter(object):
    def __init__(self):
        self.scheduler = BackgroundScheduler(timezone='Asia/Shanghai')

    def add_job(self):
        # self.scheduler.add_job(TimeHelper().get_weekday, 'interval', seconds=5)
        # self.scheduler.add_job(PlanHandle().plan_run, 'interval', seconds=10)

        self.scheduler.add_job(TestPlanVersion().plan_run, trigger='date', next_run_time=datetime.datetime.now())
        self.scheduler.add_job(KafkaUtil().kafka_run, trigger='date', next_run_time=datetime.datetime.now())
        self.scheduler.add_job(AppInfoService().delete_app_info_result, 'cron', hour=22)
        self.scheduler.add_job(MachineResourceService().machine_resource_ping, 'interval', hours=1)
        self.scheduler.add_job(TestPlanVersion().check_plan_status, 'cron', hour=23)
        # 循环调用开启摄像头抓拍
        # self.scheduler.add_job(MachineNodeService().start_machine_nodes , trigger='date', next_run_time=datetime.datetime.now())

    def run_work(self):
        self.add_job()
        self.scheduler.start()

try:
    redis_client = redis.Redis(host=Config.redis_host, port=Config.redis_port, db=Config.redis_library)
    stop_time = random.uniform(0, 1)
    time.sleep(stop_time) 
    
    if redis_client.get('scheduler_flag'):
        Logger().info('调度器已经启动---当前进程不启动', Constants.PLAN_SCHEDULE_LOG)
        scheduler = None
    else:
        redis_client.set('scheduler_flag', 'true', 2)
        Logger().info('调度器启动成功', 'scheduler.log')

        scheduler = SchedulerCenter()
        scheduler.run_work()

except Exception as e:
    Logger().info('调度器启动异常-{}'.format(e), Constants.PLAN_SCHEDULE_LOG)
