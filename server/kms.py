#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/3 22:12
# @contact : 15869300264@163.com
from models.kms.key_manager import KeyManager
from utils.exceptions.ip_exception import IPException
from utils.exceptions import BasicException
import requests


class KMS(object):
    def __init__(self, key_manager=KeyManager):
        self._key_manager = key_manager()
        self._server_url = '127.0.0.1:8045'

    def add_key(self, ip: str):
        """

        :param ip:
        :return:
        """
        try:
            sk = self._key_manager.create_sk(ip)
            self.reload_key()
            print(f'key add completed for ip:{ip}')
            print(sk)
        except IPException as e:
            print(str(e))

    def delete_key(self, keyword: str):
        """

        :param keyword:
        :return:
        """
        try:
            if self._key_manager.destroy_sk(keyword):
                self.reload_key()
                print(f'key: {keyword} had been destroyed')
            else:
                print(f'key: {keyword} does not exists!')
        except BasicException as e:
            print(str(e))

    def check_ip(self, ip: str):
        """

        :param ip:
        :return:
        """
        pass

    def reload_key(self):
        """

        :return:
        """
        try:
            requests.get(self._server_url)
        except requests.HTTPError as e:
            pass


kms = KMS()
