#!usr/bin/env python
"""
@author:keking
@file: scheduler.py
@time: 2020/04/07
@Describe:
"""
import rpyc
import logging
from app.core import request_for_xx_backend
from apscheduler.jobstores.base import JobLookupError
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.schedulers.background import BackgroundScheduler

logger = logging.getLogger("thanos-cron")

# 创建操作全局对象
scheduler = None


def init_scheduler():
    """初始化调度器"""
    logger.debug('init scheduler')

    global scheduler
    # SQLAlchemyJobStore指定存储链接
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    # 最大工作线程数20
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20},
    }
    scheduler = BackgroundScheduler()
    # scheduler.configure(executors=executors)
    # 持久化存储不支持回调函数
    scheduler.configure(jobstores=jobstores, executors=executors)
    scheduler.start()


def add_job(*args, **kwargs):
    """
    proxy： 是否需要代理
    """
    global scheduler
    jobid = kwargs.pop('id')
    try:
        scheduler.remove_job(jobid)
    except JobLookupError:
        logger.warning(f'no exist job {jobid}')
    logger.info(f'add job {jobid}')
    return scheduler.add_job(*args, id=jobid, **kwargs)


def add_job_for_proxy(*args, **kwargs):
    """
    proxy： 是否需要代理
    """
    global scheduler
    jobid = kwargs.pop('id')
    try:
        scheduler.remove_job(jobid)
    except JobLookupError:
        logger.warning(f'no exist job {jobid}')

    func = kwargs.pop('func')
    logger.info(f'add async_ job {jobid}')
    return scheduler.add_job(rpyc.async_(func), *args, id=jobid, **kwargs)


def add_job_for_request(*args, **kwargs):
    global scheduler
    jobid = kwargs.pop('id')
    try:
        scheduler.remove_job(jobid)
        logger.info(f'remove exist job {jobid}')
    except JobLookupError:
        logger.warning(f'no exist job {jobid}')
    logger.info(f'add request job {jobid}')

    # 自定制请求接口参数必须含有task_id
    task_id = kwargs.pop('task_id')
    return scheduler.add_job(request_for_xx_backend, *args, id=jobid, args=(task_id, ), **kwargs)


