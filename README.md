# 📚 学生每日扩展作业系统

一个基于 Python Flask 的学生每日作业练习系统，专为 iPad 优化，支持数学题目自动生成、答案批改、成绩统计和家长通知。

## ✨ 功能特点

- 🔢 **数学练习**：自动生成100以内加减法题目
- 📖 **语文阅读**：在线故事阅读，支持倒计时计时，确保每日阅读量
- ⏱️ **计时统计**：记录完成时间
- 📊 **成绩分析**：自动计算数学练习正确率
- 📝 **错题订正**：数学练习必须完成订正才能继续
- 📱 **iPad优化**：大字体、大按钮，适合儿童使用
- 🔔 **家长通知**：通过Server酱推送练习和阅读结果到微信

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/ChenQi/Documents/Workspace/DailyHomework
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置 (可选)

编辑 `config.py`，根据需要调整以下配置：

- `SERVERCHAN_SENDKEY`: 您的 Server酱 SendKey
- `TIANAPI_KEY`: 天行数据 API Key (用于获取更多故事内容)

> 获取 SendKey：访问 [Server酱官网](https://sct.ftqq.com/)
> 获取 API Key：访问 [天行数据](https://www.tianapi.com/)

### 3. 启动应用

```bash
python app.py
```

### 4. iPad 访问

1. 确保 iPad 和电脑连接同一个 WiFi
2. 在电脑终端查看本机 IP：`ifconfig | grep "inet "`
3. 在 iPad Safari 中访问：`http://<电脑IP>:5000`

## 📁 项目结构

```
DailyHomework/
├── app.py                 # Flask 主应用
├── config.py              # 配置文件
├── requirements.txt       # Python 依赖
├── data/                  # 数据库存储目录
│   └── database.db        # SQLite 数据库
├── generators/
│   ├── math_generator.py  # 数学题目生成器
│   └── stories.py         # 本地故事内容
├── models/
│   └── models.py          # 数据库模型与逻辑
├── services/
│   ├── notify.py          # Server酱通知服务
│   └── tianapi.py         # 天行数据接口服务
├── static/css/
│   └── style.css          # iPad 优化样式
└── templates/             # HTML 模板
    ├── index.html         # 主页
    ├── math_practice.html # 数学练习页面
    ├── result.html        # 结果展示页面
    ├── chinese_select.html# 语文阅读选择页
    └── chinese_reading.html# 语文阅读练习页
```

## ⚙️ 配置说明

编辑 `config.py` 文件：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `SERVERCHAN_SENDKEY` | `YOUR_SENDKEY` | Server酱推送密钥 |
| `MATH_QUESTION_COUNT` | `20` | 每次练习题目数量 |
| `MATH_MAX_NUMBER` | `100` | 数字范围上限 |
| `HOST` | `0.0.0.0` | 服务监听地址 |
| `PORT` | `5000` | 服务端口 |

## 📱 使用说明

1. **选择学科**：在主页选择要练习的学科（目前仅支持数学）
2. **开始练习**：系统自动生成20道题目，计时开始
3. **输入答案**：在等号后面输入答案
4. **提交批改**：点击"提交答案"按钮
5. **查看结果**：显示用时、正确率和错题
6. **订正错题**：完成所有错题订正后返回主页

## 🔔 微信通知

每次练习完成后，家长会收到包含以下信息的微信通知：

- 📅 练习日期
- ⏱️ 完成用时
- ✅ 正确数量
- ❌ 错误数量
- 📊 正确率
- 📝 错题列表（如有）

## License

MIT License
