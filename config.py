# -*- coding: utf-8 -*-
"""配置文件"""

import os
import json

# Server酱配置
# 请将 YOUR_SENDKEY 替换为您的实际 SendKey
SERVERCHAN_SENDKEY = os.environ.get('SERVERCHAN_SENDKEY', 'YOUR_SENDKEY')

# 数学题目配置
MATH_QUESTION_COUNT = int(os.environ.get('MATH_QUESTION_COUNT', 20))  # 每次练习的题目数量
MATH_MAX_NUMBER = int(os.environ.get('MATH_MAX_NUMBER', 100))         # 数字范围上限

# 数据库配置
# Docker中使用 /app/data 目录，本地开发使用当前目录
DATA_DIR = os.environ.get('DATA_DIR', os.path.dirname(__file__))
if not os.path.exists(os.path.join(DATA_DIR, 'data')):
    os.makedirs(os.path.join(DATA_DIR, 'data'), exist_ok=True)
DATABASE_PATH = os.path.join(DATA_DIR, 'data', 'database.db')

# 时区配置（默认北京时间 UTC+8）
TIMEZONE_OFFSET_HOURS = int(os.environ.get('TIMEZONE_OFFSET', 8))

# 语文阅读配置
READING_DURATION_MINUTES = int(os.environ.get('READING_DURATION', 30))  # 阅读时长（分钟）

# 天行数据API配置
# 请在 https://www.tianapi.com/ 注册获取API Key
TIANAPI_KEY = os.environ.get('TIANAPI_KEY', 'YOUR_TIANAPI_KEY')

# 内容类型配置
TIANAPI_CONTENT_TYPES = {
    'fairytales': '童话故事',
    'story': '故事大全',
    'riddle': '谜语大全',
    'rkl': '绕口令',
    'naowan': '脑筋急转弯',
    'tenwhy': '十万个为什么',
    'chengyu': '成语典故',
    'poetries': '唐诗大全',
    'poetry': '唐诗三百首'
}

# Flask配置
SECRET_KEY = os.environ.get('SECRET_KEY', 'daily-homework-secret-key-2024')
DEBUG = True
HOST = '0.0.0.0'  # 允许局域网访问
PORT = 5000

# 用户列表配置
# 从环境变量读取 JSON 格式的用户列表，默认只有一个用户"宝宝"
USERS = json.loads(os.environ.get('USERS', '["宝宝"]'))
