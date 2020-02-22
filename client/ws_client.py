#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/2/15 14:21
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
from websocket import WebSocketApp


class WsClient(object):
    def __init__(self, url: str, key: str):
        """

        :param url:
        :param key:
        """
        self._url = url
        self._key = key
        self._ws_client = WebSocketApp(self._url)

    def get_user_info(self):
        return self._ws_client.send(self._key)

    def send(self):
        """

        :return:
        """
        return self._ws_client.send(self._key)


if __name__ == '__main__':
    clinet = WsClient('ws://127.0.0.1:8045/db', '123')
    print(clinet.send())
