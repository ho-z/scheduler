#!usr/bin/env python
"""
@author:keking
@file: __init__.py.py
@time: 2020/04/07
@Describe:
"""
from app.logger import init_logger
from app.scheduler import init_scheduler
from app.tasks import init_tasks

init_logger()
init_scheduler()
init_tasks()

