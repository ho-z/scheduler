#!usr/bin/env python
"""
@author:keking
@file: service.py
@time: 2020/04/07
@Describe:
"""
import rpyc

from app.tasks.task_selenium import run
from app.scheduler import scheduler, add_job_for_proxy, add_job_for_request


class Service(rpyc.Service):
    """rpyc服务接口"""
    def exposed_add_request_job(self, *args, **kwargs):
        """通过此方法添加http请求job
        """
        return add_job_for_request(*args, **kwargs)

    def exposed_add_job(self, *args, **kwargs):
        """通过此方法添加回调job
        """
        return add_job_for_proxy(*args, **kwargs)

    def exposed_modify_job(self, job_id, jobstore=None, **changes):
        return scheduler.modify_job(job_id, jobstore, **changes)

    def exposed_reschedule_job(self, job_id, jobstore=None, trigger=None, **trigger_args):
        return scheduler.reschedule_job(job_id, jobstore, trigger, **trigger_args)

    def exposed_pause_job(self, job_id, jobstore=None):
        return scheduler.pause_job(job_id, jobstore)

    def exposed_resume_job(self, job_id, jobstore=None):
        return scheduler.resume_job(job_id, jobstore)

    def exposed_remove_job(self, job_id, jobstore=None):
        scheduler.remove_job(job_id, jobstore)

    def exposed_get_job(self, job_id):
        return scheduler.get_job(job_id)

    def exposed_get_jobs(self, jobstore=None):
        return scheduler.get_jobs(jobstore)

    def exposed_selenium(self):
        """自定义其他方式"""
        run()
        return
