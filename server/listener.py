#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/3 22:12
# @contact : 15869300264@163.com
import logging
import uuid

import tornado.ioloop
import tornado.web
import tornado.websocket
from dynaconf import settings as ds

from models.kms import key_manager

logger = logging.getLogger(__name__)


class KeyHandler(tornado.web.RequestHandler):
    def post(self):
        """

        :return:
        """
        remote_ip = self.request.remote_ip
        if remote_ip == '127.0.0.1':
            key_manager.reload_key()
            self.set_status(202)
        else:
            logger.warning(f'invalid request throw {self.request.path}, with ip: {remote_ip}')
            self.return404()

    def return404(self):
        self.set_status(404)
        self.write_error(404)


class DBHandler(tornado.websocket.WebSocketHandler):
    waiters = set()

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self):
        """
        客户端连接成功时，自动执行
        :return:
        """
        self._uid = str(uuid.uuid4())
        DBHandler.waiters.add(self)

    def on_message(self, code):
        """
        客户端连发送消息时，自动执行
        :param code:
        :return:
        """
        if key_manager.check_code(code):
            for client in DBHandler.waiters:
                client.write_message(code)
        else:
            self.write_message('code error')

    def on_close(self):
        """
        客户端关闭连接时，，自动执行
        :return:
        """
        DBHandler.waiters.remove(self)


def run(port: int = ds.get('port')):
    application = tornado.web.Application([
        (r"/db", DBHandler),
        (r"/internal", KeyHandler)
    ])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()

# if __name__ == "__main__":
#     run()
