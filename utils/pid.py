#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/3 21:12
# @contact : 15869300264@163.com
import os
from utils.exceptions.pid_exception import PidException


class Pid(object):
    path = os.getcwd()
    file_name = 'odyn.pid'
    full_path = os.path.join(path, 'conf', file_name)

    @classmethod
    def write_pid(cls):
        if os.path.isfile(cls.full_path):
            pid = cls.read_pid()
            raise PidException(f'the program had started already, with pid: {pid}')
        with open(cls.full_path, 'w') as f:
            f.write(str(os.getpid()))

    @classmethod
    def read_pid(cls):
        if os.path.isfile(cls.full_path):
            with open(cls.full_path) as f:
                return f.read()
        else:
            raise PidException('the pid file does not exist')

    @classmethod
    def delete_pid(cls):
        os.remove(cls.full_path)
