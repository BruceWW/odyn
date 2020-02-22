#!/usr/bin/env python
# -*- coding:utf-8 _*-
# @author  : Lin Luo / Bruce Liu
# @time    : 2020/1/24 10:12
# @contact : 15869300264@163.com / bruce.w.y.liu@gmail.com
from dynaconf import settings as ds

from server import kms, run
from utils import args

if __name__ == '__main__':
    if args.add is not None:
        kms.add_key(args.add)
    elif args.delete is not None:
        kms.delete_key(args.delete)
    elif args.run is True:
        run()
