# -*- coding: utf-8 -*-
"""配置文件"""

import os

# Server酱配置
# 请将 YOUR_SENDKEY 替换为您的实际 SendKey
SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY', 'YOUR_SENDKEY')

# 数学题目配置
MATH_QUESTION_COUNT = 20  # 每次练习的题目数量
MATH_MAX_NUMBER = 100     # 数字范围上限

# 数据库配置
# Docker中使用 /app/data 目录，本地开发使用当前目录
DATA_DIR = os.environ.get('DATA_DIR', os.path.dirname(__file__))
if not os.path.exists(os.path.join(DATA_DIR, 'data')):
    os.makedirs(os.path.join(DATA_DIR, 'data'), exist_ok=True)
DATABASE_PATH = os.path.join(DATA_DIR, 'data', 'database.db')

# 时区配置（默认北京时间 UTC+8）
TIMEZONE_OFFSET_HOURS = int(os.environ.get('TIMEZONE_OFFSET', 8))

# Flask配置
SECRET_KEY = os.environ.get('SECRET_KEY', 'daily-homework-secret-key-2024')
DEBUG = True
HOST = '0.0.0.0'  # 允许局域网访问
PORT = 5000
