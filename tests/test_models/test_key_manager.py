#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/2/15 18:26
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
import os
from shutil import rmtree
from unittest import TestCase

from models.kms import KeyManager
from tests.test_models.test_data import kms_correct_ip_list, kms_error_ip_list, kms_check_ip_list
from utils.exceptions import IPException


class TestKeyManager(TestCase):
    manager = KeyManager()
    file_dir = os.path.dirname(manager._key_path)

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

    def test_create_key_success(self):
        """

        :return:
        """
        for item in kms_correct_ip_list:
            sk = self.manager.create_sk(item)
            self.assertEqual(len(sk), 16)
            self.assertIsInstance(sk, str)

    def test_create_key_error_ip_fail(self):
        """

        :return:
        """
        for item in kms_error_ip_list:
            try:
                self.manager.create_sk(item)
                self.assertEqual(f'error ip {item} should not create the sk', f'ip {item} create sk successfully')
            except IPException:
                pass

    def test_check_and_destroy_success(self):
        """

        :return:
        """
        for item in kms_check_ip_list:
            sk = self.manager.create_sk(item)
            self.assertEqual(self.manager.check_sk(item, sk), True)
        for item in kms_check_ip_list:
            self.manager.destroy_sk(item)

    def test_check_fail(self):
        for item in kms_check_ip_list:
            sk = self.manager.create_sk(item)
            self.assertEqual(self.manager.check_sk('255.255.255.255', sk), False)
