#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/2/15 18:04
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
import os
from unittest import TestCase
from utils.pid import Pid, PidException
from shutil import rmtree


class TestPid(TestCase):
    pid = Pid
    file_dir = os.path.dirname(pid.full_path)

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

    def test_write_pid_success(self):
        """

        :return:
        """
        self.pid.write_pid()
        self.pid.delete_pid()

    def test_write_pid_fail(self):
        """

        :return:
        """
        self.pid.write_pid()
        try:
            self.pid.write_pid()
            self.pid.delete_pid()
            self.assertEqual('pid is not writable', 'pid is writable')
        except PidException:
            self.pid.delete_pid()

    def test_read_pid_success(self):
        """

        :return:
        """
        self.pid.write_pid()
        self.assertIsInstance(Pid.read_pid(), int)
        self.pid.delete_pid()

    def test_read_pid_fail(self):
        """

        :return:
        """
        try:
            self.pid.read_pid()
            self.pid.delete_pid()
            self.assertEqual('pid is not readable', 'pid is readable')
        except PidException:
            pass

    def test_delete_pid_success(self):
        """

        :return:
        """
        self.pid.write_pid()
        self.pid.delete_pid()
