#!/usr/bin/env python
"""
@author: Mr.zhang
@file: task_selenium.py
@time: 2020/04/07
@Describe:
"""
import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
# from selenium.webdriver.common.keys import Keys
import selenium.webdriver.support.ui as ui
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import InvalidSessionIdException
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from app import config

logger = logging.getLogger("thanos-cron")


class Runner(object):
    def __init__(self):
        self.driver = None
        self.wait = None

    def initialize(self):
        # 清除图片缓存
        chrome_options = Options()
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('window-size=1920x3000')  # 指定浏览器分辨率
        chrome_options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
        chrome_options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
        # chrome_options.add_argument('blink-settings=imagesEnabled=false') #不加载图片, 提升速度
        chrome_options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败

        self.driver = webdriver.Remote(command_executor=config.WEB_DRIVER_URL, options=chrome_options,
                                       desired_capabilities=DesiredCapabilities.CHROME)
        # self.driver = webdriver.Chrome(options=chrome_options)
        # driver.set_window_size(1920, 1000)
        # 隐式等待:在查找所有元素时，如果尚未被加载，则等5秒
        self.driver.implicitly_wait(5)
        self.wait = WebDriverWait(self.driver, 10)
        logger.debug("initialize driver completed")

    def login(self):
        """登陆"""
        logger.debug('capture login')
        self.driver.get(config.XX_FRONT_URL)
        res1 = self.driver.find_element_by_xpath('//input[@type="text"]')

        res2 = self.driver.find_element_by_xpath('//input[@type="password"]')
        res1.clear()
        res2.clear()
        res1.send_keys(config.THANOS_USERNAME)
        res2.send_keys(config.THANOS_PASSWORD)

        res3 = self.driver.find_element_by_xpath('//*[@id="login_div"]/form/div[3]/div/button')
        res3.click()
        logger.debug('login success')

    def run(self):
        """执行"""
        try:
            logger.debug('start capture.')
            self.login()
        except Exception as e:
            logger.error(f'capture err:\n{e}')
        finally:
            try:
                self.driver.close()
            except InvalidSessionIdException as e:
                logger.error(e)
                pass


def run():
    runner = Runner()

    try:
        runner.initialize()
    except Exception as e:
        logger.error(f'run capture init err:\n{e}')
        return

    runner.run()


if __name__ == '__main__':
    run()
