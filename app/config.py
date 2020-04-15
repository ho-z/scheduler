#!usr/bin/env python
"""
@author:
@file: config.py
@time: 2020/04/07
@Describe:
"""
import os
cron_env = os.environ.get('THANOS_CRON_ENV')


FILENAME = None
THANOS_USERNAME = 'xxxxxxxx'
THANOS_PASSWORD = '12345678'
WEB_DRIVER_URL = 'xxx'

if cron_env == 'local':
    XX_BACKEND_URL = 'https://xxxxxxxx'
    XX_FRONT_URL = 'https://xxxxxxxx'
    LOG_LEVEL = 10
    JIRA_CAPTURE_CRON = "*/5 * * * *"
    SEND_CAPTURE_CRON = "*/5 * * * *"

elif cron_env == 'dev':
    XX_BACKEND_URL = 'https://xxxxxxxx'
    XX_FRONT_URL = 'https://xxxxxxxx'
    LOG_LEVEL = 20
    FILENAME = "service.log"
    JIRA_CAPTURE_CRON = "30 0 * * *"
    SEND_CAPTURE_CRON = "40 0 * * *"

else:
    XX_BACKEND_URL = 'https://xxxxxxxx'
    XX_FRONT_URL = 'https://xxxxxxxx'
    LOG_LEVEL = 20
    FILENAME = "service.log"
    JIRA_CAPTURE_CRON = "30 17 * * 0-4"
    SEND_CAPTURE_CRON = "30 19 * * 0-4"
