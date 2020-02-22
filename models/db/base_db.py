#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/4 10:17
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
from abc import abstractmethod
from hashlib import sha256, md5
from time import time

from dynaconf import settings as ds

from utils.coder import Coder


class BaseDB(Coder):
    def __init__(self, key: str):
        """

        :param key:
        """
        if key is None:
            self._key = ds.get('db_key')
        else:
            self._key = key
        self._accounts = {}

    # def __del__(self):
    #     self.close()

    @abstractmethod
    def create_user(self, *args, **kwargs):
        """
        创建用户并授权
        :param args:
        :param kwargs:
        :return:
        """
        raise BaseException('this method has to be override!')

    @abstractmethod
    def sign_off_user(self, *args, **kwargs):
        """
        注销用户
        :param args:
        :param kwargs:
        :return:
        """
        raise BaseException('this method has to be override!')

    @abstractmethod
    def close(self):
        """
        销毁函数
        :return:
        """
        raise BaseException('this method has to be override!')

    def _get_account(self, key):
        """
        生产用户名和密码
        :param key:
        :return:
        """
        salt = f'{key}{self._key}{time()}'
        user = md5(salt.encode('utf-8')).hexdigest()[:8]
        password = sha256(salt.encode('utf-8')).hexdigest()[:16]
        # 生成用户名和密码，并记录到账户字典中
        self._accounts[key] = {'user': user, 'password': password}
        return user, password

    @classmethod
    def account_string(cls, user, password) -> bytes:
        """
        对用户名和密码进行encode
        :param user: 用户名
        :param password: 密码吗
        :return:
        """
        return cls.encode(f'{user}|{password}')
