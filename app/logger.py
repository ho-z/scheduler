#!usr/bin/env python
"""
@author:keking
@file: logger.py
@time: 2020/04/07
@Describe:
"""
import os
import logging

from app.config import FILENAME, LOG_LEVEL

cron_env = os.environ.get('THANOS_CRON_ENV')


def init_logger():
    """创建logger对象"""
    logger = logging.getLogger("thanos-cron")
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s in %(module)s: %(message)s")
    if cron_env == 'local':
        handler = logging.StreamHandler()
    else:
        handler = logging.FileHandler(filename=FILENAME)

    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(LOG_LEVEL)
