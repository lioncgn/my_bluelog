#!/usr/bin/env python
# -*- coding=utf-8 -*-

#安装python-dotenv，使用flask run 命令启动开发服务器时Flask会自动导入存储在.flaskenv 或者.env中的环境变量
#在生产环境下，不能再使用这个命令启动程序，因此需要手动导入环境变量
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from bluelog import create_app
app = create_app('production')
