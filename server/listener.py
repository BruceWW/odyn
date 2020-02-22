#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/3 22:12
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
import logging
import uuid
from importlib import import_module

import tornado.ioloop
import tornado.web
import tornado.websocket
from dynaconf import settings as ds

from utils.coder import version_manage
from models.kms import KeyManager
from utils.exceptions import BasicException

logger = logging.getLogger(__name__)

key_manager = KeyManager()


class KeyHandler(tornado.web.RequestHandler):
    def get(self):
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
    code = None
    module = import_module(ds.MODULE)
    tmp = eval(f'module.{ds.DB_CLIENT}')
    db_client = tmp()

    def check_origin(self, origin: str) -> bool:
        return True

    def open(self):
        """
        客户端连接成功时，自动执行
        :return:
        """
        self._uid = str(uuid.uuid4())

    def on_message(self, code):
        """
        客户端连发送消息时，自动执行
        :param code:
        :return:
        """
        request_ip = self.request.remote_ip
        if key_manager.check_sk(request_ip, code):
            try:
                info = self.db_client.create_user(code, request_ip, 'all', 'city_uv')
                self.code = code
                self.write_message(version_manage(str(info, 'utf-8'), 200))
            except BasicException as e:
                self.write_message(str(e))
        else:
            self.write_message('code error')

    def on_close(self):
        """
        客户端关闭连接时，，自动执行
        :return:
        """
        if self.code is not None:
            self.db_client.sign_off_user(self.code)


def run(port: int = ds.get('port')):
    application = tornado.web.Application([
        (r"/db", DBHandler),
        (r"/internal", KeyHandler)
    ])
    application.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    print(123)
    run()
