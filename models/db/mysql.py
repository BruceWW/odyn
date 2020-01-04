#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/4 10:12
# @contact : 15869300264@163.com

from json import dump
from models.db.base_db import BaseDB
import pymysql
from dynaconf import settings as ds
import os


class MySql(BaseDB):
    def __init__(self, host: str, port: int, user: str, password: str, key: str = None):
        """

        :param host:
        :param port:
        :param user:
        :param password:
        :param key:
        """
        super().__init__(key)
        self._conn = pymysql.connect(host=host, port=port, user=user, password=password)
        self._cursor = self._conn.cursor()
        self._create_account = 'create user "{user}"@"{ip}" identified by "{password}";'
        self._grant_privileges = 'grant {privileges} privileges on "{db}".{table} to "{user}"@"{ip}" identified by "{password}";'
        self._delete_account = 'delete from mysql.user where user == "{user}";'
        self._delete_accounts = "delete from mysql.user where user in ({users});"
        self._flush = 'flush privileges;'
        self._users = []
        self._user_path = os.path.join(os.getcwd(), 'conf', 'user.json')

    def _dump_file(self):
        """

        :return:
        """
        with open(self._user_path, 'w', encoding='utf-8') as f:
            dump(f, self._users, ensure_ascii=False)

    def create_user(self, key: str, ip: str, privileges: str, db: str, tables: str = '*') -> str:
        """

        :param key:
        :param ip:
        :param privileges:
        :param db:
        :param tables:
        :return:
        """
        user, password = self._get_account(key)
        try:
            self._cursor.execute(self._create_account.format(user=user, ip=ip, password=password))
            self._cursor.execute(
                self._grant_privileges.format(db=db, table=tables, user=user, password=password, ip=ip,
                                              privileges=privileges))
            self._cursor.execute(self._flush)
            self._users.append(user)
            self._dump_file()
            return self.account_string(user=user, password=password)
        except BaseException as e:
            print(str(e))

    def sign_off_user(self, key):
        """

        :param key:
        :return:
        """
        user = self._accounts.get(key)
        if user is None:
            print('error')
        else:
            try:
                self._cursor.execute(self._delete_account.format(user=user['user']))
                self._cursor.execute(self._flush)
                self._users.remove(user)
                self._dump_file()
            except BaseException as e:
                print(str(e))

    def close(self):
        self.__del__()

    def __del__(self):
        """

        :return:
        """
        if len(self._accounts) == 0:
            return
        users = ','.join(f'"{self._accounts[user]["user"]}"' for user in self._accounts)
        self._cursor.execute(self._delete_accounts.format(users=users))
        self._cursor.execute(self._flush)
        os.remove(self._user_path)


client = MySql(host=ds.get('db_host'), port=ds.get('db_port'), user=ds.get('db_user'),
               password=ds.get('db_password'))
# if __name__ == '__main__':
#     client = MySql(host='127.0.0.1', port=3306, user='root', password='root')
#     client.create_user('hi', '127.0.0.1', 'all', 'midend_adimn', '*')
#     client.close()
