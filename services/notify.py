# -*- coding: utf-8 -*-
"""Server酱通知服务"""

import requests
from datetime import datetime

import config


def send_practice_result(result: dict) -> bool:
    """
    发送练习结果通知到家长微信
    
    Args:
        result: 练习结果字典，包含 accuracy, duration_display, correct, total, wrong_questions
        
    Returns:
        是否发送成功
    """
    if config.SERVERCHAN_UID == 'YOUR_UID' or config.SERVERCHAN_SENDKEY == 'YOUR_SENDKEY':
        print("警告: Server酱 UID 或 SendKey 未配置，跳过通知发送")
        return False
    
    # 防止重复发送
    practice_id = result.get('practice_id')
    if practice_id:
        from models.models import is_practice_notified, mark_practice_notified
        if is_practice_notified(practice_id):
            print(f"练习 {practice_id} 已发送过通知，跳过")
            return False
    
    # 构建消息标题
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    title = f"📝 {date_str} 数学练习完成"
    
    # 构建消息内容
    accuracy = result.get('accuracy', 0)
    emoji = "🎉" if accuracy >= 90 else "👍" if accuracy >= 70 else "💪"
    
    content = f"""
## {emoji} 练习报告

| 项目 | 结果 |
|------|------|
| 📅 日期 | {date_str} |
| ⏱️ 用时 | {result.get('duration_display', '-')} |
| ✅ 正确 | {result.get('correct', 0)} 题 |
| ❌ 错误 | {result.get('wrong', 0)} 题 |
| 📊 正确率 | **{accuracy}%** |

"""
    
    # 如果有错题，列出来
    wrong_questions = result.get('wrong_questions', [])
    if wrong_questions:
        content += "\n### ❌ 错题列表\n\n"
        for q in wrong_questions:
            content += f"- {q['display']} 答案应为 **{q['correct_answer']}**，填写了 {q['user_answer']}\n"
        content += "\n> 请督促小朋友订正错题哦～"
    else:
        content += "\n> 🌟 全部正确，太棒了！"
    
    # 发送请求 (Server酱³)
    url = f"https://{config.SERVERCHAN_UID}.push.ft07.com/send/{config.SERVERCHAN_SENDKEY}.send"
    
    try:
        response = requests.post(url, data={
            'title': title,
            'desp': content
        }, timeout=10)
        
        result_json = response.json()
        if result_json.get('code') == 0:
            print(f"通知发送成功")
            # 标记已通知
            if practice_id:
                mark_practice_notified(practice_id)
            return True
        else:
            print(f"通知发送失败: {result_json}")
            return False
            
    except Exception as e:
        print(f"通知发送异常: {e}")
        return False



if __name__ == '__main__':
    # 测试
    test_result = {
        'accuracy': 85.0,
        'duration_display': '3分25秒',
        'correct': 17,
        'wrong': 3,
        'total': 20,
        'wrong_questions': [
            {'display': '45 + 38 = ', 'correct_answer': 83, 'user_answer': 73},
            {'display': '67 - 29 = ', 'correct_answer': 38, 'user_answer': 48},
            {'display': '92 - 58 = ', 'correct_answer': 34, 'user_answer': 44}
        ]
    }
    send_practice_result(test_result)


def send_reading_result(result: dict) -> bool:
    """
    发送阅读完成通知到家长微信
    
    Args:
        result: 阅读结果字典
        
    Returns:
        是否发送成功
    """
    if config.SERVERCHAN_UID == 'YOUR_UID' or config.SERVERCHAN_SENDKEY == 'YOUR_SENDKEY':
        print("警告: Server酱 UID 或 SendKey 未配置，跳过通知发送")
        return False
    
    now = datetime.now()
    date_str = now.strftime('%Y年%m月%d日')
    title = f"📖 {date_str} 语文阅读完成"
    
    content = f"""
## 🎉 阅读完成报告

| 项目 | 内容 |
|------|------|
| 📅 日期 | {date_str} |
| 📚 故事 | {result.get('story_title', '-')} |
| ⏱️ 阅读时长 | {result.get('duration_display', '-')} |

> 🌟 小朋友完成了今天的阅读任务，太棒了！
"""
    
    url = f"https://{config.SERVERCHAN_UID}.push.ft07.com/send/{config.SERVERCHAN_SENDKEY}.send"
    
    try:
        response = requests.post(url, data={
            'title': title,
            'desp': content
        }, timeout=10)
        
        result_json = response.json()
        if result_json.get('code') == 0:
            print(f"阅读通知发送成功")
            return True
        else:
            print(f"阅读通知发送失败: {result_json}")
            return False
            
    except Exception as e:
        print(f"阅读通知发送异常: {e}")
        return False
