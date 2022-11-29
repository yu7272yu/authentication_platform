# coding=utf-8


class Config(object):
    """
    平台配置信息
    """

    # mysql 配置信息
    mysql_host = 'localhost'
    mysql_port = 3306
    mysql_user = 'root'
    mysql_password = '123456'
    mysql_db = 'video3'

    # reids配置信息
    redis_host = 'localhost'
    redis_port = 6379
    redis_library = 0
    
    # kafka配置信息
    kafka_host = '161.189.73.195'
    kafka_port = 9092
    topic_test01 = 'text1'
    topic_algorithm_face = 'deepstream'
    topic_smart_face = 'machina_resource'   # 小摄像头平台消费
    topic_algo_face_memory = 'kb_irs_hit-alarm-upload-topic'   # 推送到算法平台存储到内存中
    topic_algo_update_memory = 'kb_irs_alarm-topic'       # 接收算法平台推送的结果
    topic_error_msg = 'error'


    # fdfs配置信息
    fdfs_host = False
    fdfs_nginx_ip = "http://161.189.73.195:8888/"
    fdfs_nginx_port = 8888

    # 算法服务器信息配置 --config
    algorithm_face_host = '192.168.100.203'
    algorithm_face_post = 6002

    # 算法服务器信息配置 --config
    algorithm_car_host = '192.168.100.203'
    algorithm_car_post = 6002

    # 算法服务器信息配置 --config
    algorithm_park_host = '192.168.100.203'
    algorithm_park_post = 6002

    # 算法服务器信息配置 --config
    algorithm_parkptz_host = '192.168.100.203'
    algorithm_parkptz_post = 6002

    # 算法服务器信息配置 --config
    algorithm_fire_host = '192.168.100.203'
    algorithm_fire_post = 6002

    # 算法服务器信息配置 --config
    algorithm_check_host = '192.168.100.203'
    algorithm_check_post = 6002

    # 小摄像头平台
    smart_camera_host = ''
    smart_camera_port = ''

    # app_list 定义
    app_name_list = ['违停', '区间测速', '以脸搜脸', '轨迹查询', '黑名单布控', '白名单布控', '烟火检测', '区域入侵', '奔跑检测', '行进方向检测']

    #流媒体服务器相关
    zlm_url = "http://161.189.73.195"
    zlm_port = "8180"
    
    # 厂家
    manufacturer_name_list = ['海康威视', '大华', '宇视', '索尼', '安讯士', '博世', '寰旭']
    # 设备类型 
    machine_type_list = ['枪机', '球机', '半球', '小摄像头']
    # 阈值名称
    threshold_type_list = ['检测阈值', '违停时间阈值','限速阈值', '短信提示阈值', '删除阈值', '速度阈值', '人数阈值', '人车数量阈值', '人车停留时间阈值', '单位时间阈值', '变化量阈值']

    # algo调用人脸
    algo_face_host = "192.168.100.202"
    algo_face_port = "9999"
