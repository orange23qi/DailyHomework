# 📚 学生每日扩展作业系统

一个基于 Python Flask 的学生每日作业练习系统，专为 iPad 优化，支持数学题目自动生成、答案批改、成绩统计和家长通知。

## ✨ 功能特点

- 🔢 **数学练习**：自动生成100以内加减法题目
- ⏱️ **计时统计**：记录完成时间
- 📊 **成绩分析**：自动计算正确率
- 📝 **错题订正**：必须完成订正才能继续
- 📱 **iPad优化**：大字体、大按钮，适合儿童使用
- 🔔 **家长通知**：通过Server酱推送练习结果到微信

## 🚀 快速开始

### 1. 安装依赖

```bash
cd /Users/ChenQi/Documents/Workspace/DailyHomework
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. 配置 Server酱 (可选)

编辑 `config.py`，将 `YOUR_SENDKEY` 替换为您的 Server酱 SendKey：

```python
SERVERCHAN_SENDKEY = '您的SendKey'
```

> 获取 SendKey：访问 [Server酱官网](https://sct.ftqq.com/)

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
├── database.db           # SQLite 数据库（自动生成）
├── generators/
│   └── math_generator.py  # 数学题目生成器
├── models/
│   └── models.py          # 数据库模型
├── services/
│   └── notify.py          # Server酱通知服务
├── static/css/
│   └── style.css          # iPad 优化样式
└── templates/
    ├── index.html         # 主页
    ├── math_practice.html # 数学练习页面
    └── result.html        # 结果展示页面
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
