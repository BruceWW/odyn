#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/4 11:12
# @contact : 15869300264@163.com
import logging
import os
import uuid
from hashlib import sha256
from json import load, dump
from json.decoder import JSONDecodeError
from shutil import copyfile
from time import time

from IPy import IP

from utils.exceptions.ip_exception import IPException

logger = logging.getLogger(__name__)


class KeyManager(object):
    def __init__(self):
        self._key_path = os.path.join(os.getcwd(), 'conf', 'key.json')
        self._keys = {}
        self._load_key()

    def _load_key(self):
        if os.path.isfile(self._key_path):
            try:
                with open(self._key_path, 'r') as f:
                    self._keys = load(f)
            except JSONDecodeError as e:
                bak_path = os.path.join(f'{self._key_path}-{time()}-bak')
                copyfile(self._key_path, bak_path)
                logger.error(f'{str(e)}, and the error file had been restore with named {bak_path}')
                self._keys = {}

    def _dump_file(self):
        with open(self._key_path, 'w') as f:
            dump(self._keys, f, ensure_ascii=False)

    def reload_key(self):
        if os.path.isfile(self._key_path):
            try:
                with open(self._key_path, 'r') as f:
                    self._keys = load(f)
            except JSONDecodeError as e:
                bak_path = os.path.join(f'{self._key_path}-{time()}-bak')
                copyfile(self._key_path, bak_path)
                logger.error(f'{str(e)}, and the error file had been restore with named {bak_path}')

    def check_sk(self, request_ip, sk):
        """

        :param request_ip:
        :param sk:
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

        :param keyword:
        :return:
        """
        if keyword is None:
            return False
        elif self._keys.get(keyword) is not None:
            self._keys.pop(keyword)
            self._dump_file()
            return True
        elif keyword in self._keys.values():
            self._keys = {k: v for k, v in self._keys.items() if v != keyword}
            self._dump_file()
            return True
        else:
            return False

    def create_sk(self, ip):
        """

        :param ip:
        :return:
        """
        try:
            IP(ip)
        except ValueError as e:
            raise IPException(f'ip: {ip} error with info: {str(e)}')
        sk = sha256(str(uuid.uuid4()).encode('utf-8')).hexdigest()[:16]
        self._keys[sk] = ip
        self._dump_file()
        return sk
