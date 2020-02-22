#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/2/15 15:19
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
from client.db_user_decoder import UserDecoder
from unittest import TestCase


class TestDecoder(TestCase):
    def test_decode(self):
        info = 'MS4wfDIwMHxaV1ZoWWpVNE16TjhNMkl6TXpRNE1URXhPVFZpWVdSa1pRPT0 ='
        res = UserDecoder.decode(info)
        self.assertTupleEqual(res, ('eeab5833', '3b334811195badde'))
