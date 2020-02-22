#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/15 22:04
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com


class BasicException(BaseException):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return f'{self.__class__.__name__}: {str(self._msg)}'
