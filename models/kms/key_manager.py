#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/4 11:12
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
import logging
import os
import uuid
from hashlib import sha256
from json import loads, dumps
from json.decoder import JSONDecodeError
from shutil import copyfile
from time import time

from IPy import IP

from utils.coder import Coder
from utils.exceptions import IPException, KmsException

logger = logging.getLogger(__name__)


class KeyManager(Coder):
    def __init__(self):
        self._key_path = os.path.join(os.getcwd(), 'conf', 'key.info')
        self._keys = {}
        self._load_key()

    def _load_key(self) -> None:
        """
        加载密钥
        判断是否有密钥文件，如果有则加载，否则跳过
        如果加载过程中出现异常，则备份当前密钥文件，并清空所有密钥
        :return:
        """
        if os.path.isfile(self._key_path):
            try:
                with open(self._key_path, 'r') as f:
                    self._keys = loads(self.decode(f.readline().encode('utf-8')))
            except JSONDecodeError as e:
                bak_path = os.path.join(f'{self._key_path}-{time()}-bak')
                copyfile(self._key_path, bak_path)
                logger.error(f'{str(e)}, and the error file had been restore with named {bak_path}')
                self._keys = {}

    def _dump_file(self) -> None:
        """
        更新密钥文件
        :return:
        """
        with open(self._key_path, 'w') as f:
            f.write(str(self.encode(dumps(self._keys)), 'utf-8'))

    def reload_key(self) -> None:
        """
        重新加载密钥，
        如果没有密钥文件，会根据当前密钥重新生成
        如果出现异常，备份当前密钥文件，
        且不会清空原有密钥
        :return:
        """
        if os.path.isfile(self._key_path):
            self._load_key()
        else:
            self._dump_file()
            raise KmsException('key file not exists, please check it')

    def check_sk(self, request_ip: str, sk: str) -> bool:
        """
        校验密钥与请求ip是否符合
        :param request_ip: 请求的发起的ip
        :param sk: 密钥
        :return:
        """
        ip = self._keys.get(sk)
        if ip is None:
            return False
        elif request_ip in IP(ip):
            return True
        else:
            return False

    def destroy_sk(self, keyword: str = None) -> bool:
        """
        通过ip或密钥进行销毁
        并刷新密钥存储文件
        :param keyword: 销毁关键字
        :return: 如果销毁成功，返回True；销毁失败返回False
        """
        if keyword is None:
            return False
        elif self._keys.get(keyword) is not None:
            # 如果传入的关键字是密钥
            self._keys.pop(keyword)
            self._dump_file()
            return True
        elif keyword in self._keys.values():
            # 如果传入的关键字是ip
            self._keys = {k: v for k, v in self._keys.items() if v != keyword}
            self._dump_file()
            return True
        else:
            return False

    def create_sk(self, ip: str) -> str:
        """
        生成密钥，并刷新密钥存储文件
        :param ip:
        :return: 生成的密钥
        """
        try:
            IP(ip)
        except ValueError as e:
            raise IPException(f'ip: {ip} error with info: {str(e)}')
        sk = sha256(str(uuid.uuid4()).encode('utf-8')).hexdigest()[:16]
        self._keys[sk] = ip
        self._dump_file()
        return sk
