#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/2/15 12:08
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
from base64 import b64decode

version = '1.0'


class DecoderException(BaseException):
    def __init__(self, msg):
        self._msg = msg

    def __str__(self):
        return f'{self.__class__.__name__}: {str(self._msg)}'


class UserDecoder(object):
    @staticmethod
    def _decoder_v1(info: str) -> tuple:
        """

        :param info:
        :return:
        """
        return tuple(b64decode(info).decode('utf-8').split('|'))

    @classmethod
    def decode(cls, user_info: str) -> tuple:
        """
        解码用户信息
        :param user_info: 用户信息（用户名，密码）
        :return:
        """
        try:
            user_info = b64decode(user_info).decode('utf-8')
            tmp = user_info.split('|')
            if len(tmp) == 2:
                return tuple(tmp)
            if tmp[1] == '200':
                if tmp[0] == '1.0':
                    return cls._decoder_v1(tmp[2])
                else:
                    raise DecoderException(f'decoder version error, version: {tmp[0]} required!')
            else:
                raise DecoderException(f'result status_code error, with error code: {tmp[1]}')
        except IndexError:
            raise DecoderException('response info error')
        except BaseException as e:
            raise DecoderException(str(e))
