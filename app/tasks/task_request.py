#!usr/bin/env python
"""
@author:keking
@file: task_request.py
@time: 2020/03/12
@Describe:
"""
import logging
import requests

from app import config

logger = logging.getLogger("thanos-cron")


def send():
    data = {
        "send_to": "center",
    }
    try:
        res = requests.post(f"{config.XX_BACKEND_URL}/monitor/send-monitor-capture", json=data)
        logger.info(f'send monitor capture code:{res.status_code}')
        logger.info(res.text)
    except requests.exceptions.ConnectionError:
        logger.error('send monitor connect error')


if __name__ == '__main__':
    send()
