#!/usr/bin/env python
"""
@author: Mr.zhang
@file: __init__.py.py
@time: 2020/04/07
@Describe: 可以把一些和其他业务不相关的定时任务写在此服务内
"""
import os
import logging
from app import config
from .task_selenium import run
from .task_request import send

from app.scheduler import add_job

cron_env = os.environ.get('THANOS_CRON_ENV')

logger = logging.getLogger("thanos-cron")


def from_crontab(cron):
    values = cron.split(' ')
    return {
        'minute': values[0],
        'hour': values[1],
        'day': values[2],
        'month': values[3],
        'day_of_week': values[4],
    }


def init_tasks():
    logger.debug('init tasks')

    add_job(
        func=run, id=f'{cron_env}_JIRA_CAPTURE', args=(), trigger='cron', **from_crontab(config.JIRA_CAPTURE_CRON)
    )
    add_job(
        func=send, id=f'{cron_env}_SEND_CAPTURE', args=(), trigger='cron', **from_crontab(config.SEND_CAPTURE_CRON)
    )
