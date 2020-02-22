#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/2/15 18:10
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
from base64 import b64decode, b64encode

version = '1.0'


class Coder(object):
    @staticmethod
    def encode(data: str) -> bytes:
        """

        :param data:
        :return:
        """
        return b64encode(data.encode('utf-8'))

    @staticmethod
    def decode(data: bytes) -> str:
        """

        :param data:
        :return:
        """
        return b64decode(data).decode('utf-8')


def version_manage(data: str, status_code: int = 200) -> str:
    """

    :param data:
    :param status_code:
    :return:
    """
    info = '%s|%d|%s' % (version, status_code, data)
    return str(b64encode(info.encode('utf-8')), 'utf-8')
