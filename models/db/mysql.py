#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/4 10:12
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com

import logging
import os
from json import dumps, loads
from json.decoder import JSONDecodeError
from shutil import copyfile
from dynaconf import settings as ds
from time import time

import pymysql

from models.db.base_db import BaseDB
from utils.exceptions import DbException

logger = logging.getLogger(__name__)


class MySql(BaseDB):
    def __init__(self, host: str = None, port: int = None, user: str = None, password: str = None,
                 key: str = None, strict: bool = False):
        """
        mysql操作类
        :param host: mysql主机ip，默认127.0.0.1
        :param port: mysql端口，默认3306
        :param user: mysql用户名，默认root
        :param password: mysql用户，默认root
        :param key: 预置盐值
        :param strict: 是否安全模式，如果是True，则传入重复的key时，会删除对应key的账户；
        """
        super().__init__(key)
        if host is None:
            host = ds.DB_HOST
        if port is None:
            port = ds.DB_PORT
        if user is None:
            user = ds.DB_USER
        if password is None:
            password = ds.DB_PASSWORD
        self._conn = pymysql.connect(host=host, port=port, user=user, password=password)
        self._cursor = self._conn.cursor()
        self._create_account = 'create user "{user}"@"{ip}" identified by "{password}";'
        self._grant_privileges = 'grant {privileges} privileges on {db}.{table} to "{user}"@"{ip}" identified by "{password}";'
        self._delete_account = "delete from mysql.user where user = '{user}';"
        self._delete_accounts = "delete from mysql.user where user in ({users});"
        self._flush = 'flush privileges;'
        self._users = []
        self._user_path = os.path.join(os.getcwd(), 'conf', 'mysql-user.info')
        if os.path.isfile(self._user_path):
            self._load_file()
        self._strict = strict

    def _dump_file(self):
        """
        更新权限记录表
        :return:
        """
        with open(self._user_path, 'w', encoding='utf-8') as f:
            f.write(str(self.encode(dumps(self._accounts)), 'utf-8'))

    def _load_file(self):
        """
        获取已存在的记录信息
        :return:
        """
        with open(self._user_path, 'r', encoding='utf-8') as f:
            try:
                self._accounts = loads(self.decode(f.readline().encode('utf-8')))
                self._users = [value['user'] for value in self._accounts.values()]
            except JSONDecodeError as e:
                bak_path = os.path.join(f'{self._user_path}-{time()}-bak')
                copyfile(self._user_path, bak_path)
                logger.error(f'{str(e)}, and the error file had been restore with named {bak_path}')
                self._accounts = {}
                self._users = []

    def _check_key(self, key: str, strict: bool = False) -> bool:
        """
        检查key是否重复
        :param key:
        :param strict:
        :return: 如果存在则返回True，不存在则返回False
        """
        if strict is False:
            return key in self._accounts.keys()
        else:
            if key in self._accounts.keys():
                # 如果为安全模式，且key重复，则删除之前的账户
                self.sign_off_user(key)
                return True
            else:
                return False

    def create_user(self, key: str, ip: str, privileges: str, db: str, tables: str = '*') -> bytes:
        """
        创建用户
        :param key: 用户盐值
        :param ip: 请求方ip
        :param privileges: 权限信息
        :param db: 数据库名称
        :param tables: 表名称，默认全部
        :return:
        """
        if self._check_key(key) is True:
            logger.warning(f'key: {key} had been used!')
            raise DbException(f'key: {key} had been used!')
        # 生成用户名和密码
        user, password = self._get_account(key)
        try:
            self._conn.begin()
            # 创建账户
            self._cursor.execute(self._create_account.format(user=user, ip=ip, password=password))
            # 执行授权
            self._cursor.execute(
                self._grant_privileges.format(db=db, table=tables, user=user, password=password, ip=ip,
                                              privileges=privileges))
            # 刷新权限
            self._cursor.execute(self._flush)
            # 添加账户记录信息
            self._users.append(user)
            # 刷新本地记录文件
            self._dump_file()
            self._conn.commit()
            # 返回账户信息
            return self.account_string(user=user, password=password)
        except BaseException as e:
            self._accounts.pop(key)
            logger.error(f'create_user error: {str(e)}')
            self._conn.rollback()
            raise DbException(f'create_user error: {str(e)}')

    def sign_off_user(self, key: str) -> bool:
        """
        注销用户
        :param key:
        :return:
        """
        try:
            # 根据key获取用户名
            user = self._accounts[key]
            # 删除账户
            self._cursor.execute(self._delete_account.format(user=user['user']))
            # 刷新账户信息
            self._cursor.execute(self._flush)
            self._users.remove(user['user'])
            self._accounts.pop(key)
            self._dump_file()
            return True
        except KeyError:
            logger.warning(f'sign_off_user key: {key} does not exist')
            raise DbException(f'sign_off_user key: {key} does not exist')
        except BaseException as e:
            logger.error(f'sign_off_user error: {str(e)}')
            raise DbException(f'sign_off_user error: {str(e)}')

    def close(self) -> None:
        """
        销毁函数
        :return:
        """
        # 判断账户信息是否为空
        if len(self._accounts) == 0:
            return
        else:
            # 获取用户清单
            try:
                self._conn.begin()
                users = ','.join(self._users)
                self._cursor.execute(self._delete_accounts.format(users=users))
                self._cursor.execute(self._flush)
                self._conn.commit()
                os.remove(self._user_path)
            except BaseException as e:
                logger.error(f'MySqlDB delete users failed with error: {str(e)}')
                self._conn.rollback()
                raise DbException(f'MySqlDB delete users failed with error: {str(e)}')

# client = MySql(host=ds.get('db_host'), port=ds.get('db_port'), user=ds.get('db_user'),
#                password=ds.get('db_password'))
