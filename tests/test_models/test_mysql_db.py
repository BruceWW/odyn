#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/2/15 19:37
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
import os
from shutil import rmtree
from unittest import TestCase

from models.db import MySql
from client.db_user_decoder import UserDecoder


class TestMysqlDb(TestCase):
    mysql_db = MySql()
    file_dir = os.path.dirname(mysql_db._user_path)

    @classmethod
    def setUpClass(cls) -> None:
        """

        :return:
        """
        if not os.path.isdir(cls.file_dir):
            os.mkdir(cls.file_dir)

    @classmethod
    def tearDownClass(cls) -> None:
        """

        :return:
        """
        rmtree(cls.file_dir)

    def test_create_user(self):
        """

        :return:
        """
        key = 'this is test key'
        ip = '172.17.0.1'
        privileges = 'all'
        db = 'city_uv'
        info = self.mysql_db.create_user(key, ip, privileges, db)
        print(UserDecoder.decode(info))
        self.assertEqual(len(UserDecoder.decode(info)), 2)
        self.assertEqual(self.mysql_db.sign_off_user(key), True)
