#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/4 10:17
# @contact : 15869300264@163.com
from abc import abstractmethod
from hashlib import sha256, md5
from base64 import b64encode
from time import time
from dynaconf import settings as ds


class BaseDB(object):
    @abstractmethod
    def __init__(self, key: str):
        """

        :param key:
        """
        if key is None:
            self._key = ds.get('db_key')
        else:
            self._key = key
        self._accounts = {}

    @abstractmethod
    def create_user(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def sign_off_user(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :return:
        """
        pass

    @abstractmethod
    def close(self):
        """

        :return:
        """
        pass

    def _get_account(self, key):
        """

        :param key:
        :return:
        """
        new_key = f'{key}{self._key}{time()}'
        user = md5(new_key.encode('utf-8')).hexdigest()[:8]
        password = sha256(new_key.encode('utf-8')).hexdigest()[:16]
        self._accounts[key] = {'user': user, 'password': password}
        return user, password

    @staticmethod
    def account_string(user, password):
        """

        :param user:
        :param password:
        :return:
        """
        return b64encode(f'{user}|{password}'.encode('utf-8'))
