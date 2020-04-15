#!usr/bin/env python
"""
@author:keking
@file: main.py
@time: 2020/04/07
@Describe:
"""
import os
import logging
from rpyc.utils.server import ThreadedServer

os.environ.setdefault("THANOS_CRON_ENV", "local")  # 本地环境
# os.environ.setdefault("THANOS_CRON_ENV", "prod")  # 线上环境
# os.environ.setdefault("THANOS_CRON_ENV", "dev")  # 开发测试环境


def main():
    from app.service import Service
    from app.scheduler import scheduler
    logger = logging.getLogger("thanos-cron")

    protocol_config = {'allow_public_attrs': True, 'sync_request_timeout': 120}
    server = ThreadedServer(Service, port=9999, protocol_config=protocol_config)
    try:
        logger.info('server start')
        server.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info('server down')
        pass
    finally:
        scheduler.shutdown()


if __name__ == '__main__':
    main()
