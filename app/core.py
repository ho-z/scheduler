#!usr/bin/env python
"""
@author:keking
@file: core.py
@time: 2020/04/15
@Describe:
"""
import coreapi
import logging
import requests
from app import config

logger = logging.getLogger("thanos-cron")

# Initialize a client & load the schema document
client = coreapi.Client()

# Interact with the API endpoint
action = ["api-token-auth", "create"]


def get_django_token():
    """获取django平台token认证"""
    data = {
        "username": config.THANOS_USERNAME,
        "password": config.THANOS_PASSWORD,
    }
    # schema = None
    schema = client.get(config.XX_BACKEND_URL)
    try:
        result = client.action(schema, action, params=data)
    except coreapi.exceptions.ErrorMessage as exc:
        logging.error(f"request error: \n{exc}")
        return
    except Exception as exc:
        logging.error(f"request error: \n{exc}")
        return
    return result["token"]


def request_for_xx_backend(task_id):
    """请求某某后端服务"""
    # 如果后端是django项目，可以采用此方式获取认证token
    token = get_django_token()
    headers = {
        'Token': token,
        "username": config.THANOS_USERNAME
    }
    params = {
        "task_id": task_id
    }
    try:
        # 调用接口，传入指定task_id，另一端服务调起任务执行
        res = requests.get(f"{config.XX_BACKEND_URL}/tasks/run-task", params=params, headers=headers)
    except ConnectionError:
        logging.error(f'TASK - {task_id}, connect backend error')
        return 
    logger.info(f'TASK - {task_id}, request-result:\n{res}')
    return


def request_for_xxxx(task_id):
    """支持多个平台的任务请求"""
    pass
