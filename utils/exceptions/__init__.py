#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/3 21:16
# @contact : 15869300264@163.com


class BasicException(BaseException):
    def __init__(self, msg):
        self._msg = msg

    def __str(self):
        return f'{self.__name__}: {str(self._msg)}'
