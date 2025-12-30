# -*- coding: utf-8 -*-
"""
学生每日扩展作业 - Flask 主应用
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

import config
from generators.math_generator import generate_questions
from generators.stories import get_today_story, get_story_by_id, get_random_story
from models.models import (
    create_practice, submit_practice, submit_corrections,
    get_practice_history, get_practice_history_by_days, get_math_stats_for_chart,
    create_reading_record, complete_reading
)
from services.notify import send_practice_result, send_reading_result

app = Flask(__name__)
app.secret_key = config.SECRET_KEY

# Session Cookie 配置（Safari 兼容）
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
app.config['SESSION_COOKIE_SECURE'] = False  # HTTP 环境下需要设为 False
app.config['SESSION_COOKIE_HTTPONLY'] = True


def get_current_user():
    """获取当前用户名（从 session 获取，默认第一个用户）"""
    user = session.get('current_user')
    if not user or user not in config.USERS:
        user = config.USERS[0] if config.USERS else '宝宝'
        session['current_user'] = user
    return user


@app.route('/switch-user')
def switch_user():
    """切换用户"""
    user_name = request.args.get('user', '')
    if user_name in config.USERS:
        session['current_user'] = user_name
        # 返回 JSON 响应，由前端处理刷新
        return jsonify({'success': True, 'user': user_name})
    return jsonify({'success': False})


@app.route('/')
def index():
    """主页 - 学科分类"""
    current_user = get_current_user()
    # 获取最近7天的练习记录（按当前用户筛选）
    history = get_practice_history_by_days(7, user_name=current_user)
    # 获取数学统计图表数据（按当前用户筛选）
    math_stats = get_math_stats_for_chart(7, user_name=current_user)
    return render_template('index.html', 
                         history=history, 
                         math_stats=math_stats,
                         users=config.USERS,
                         current_user=current_user)


@app.route('/math')
def math_practice():
    """数学练习页面"""
    current_user = get_current_user()
    # 生成题目
    questions = generate_questions(
        count=config.MATH_QUESTION_COUNT,
        max_number=config.MATH_MAX_NUMBER
    )
    
    # 创建练习记录（关联当前用户）
    practice_id = create_practice('数学', questions, user_name=current_user)
    
    # 只保存验证所需的最小数据到 session（减少 cookie 大小，解决 Safari 兼容问题）
    session['answers'] = {q['id']: q['answer'] for q in questions}
    session['practice_id'] = practice_id
    
    return render_template('math_practice.html', 
                         questions=questions, 
                         practice_id=practice_id,
                         current_user=current_user)


@app.route('/math/submit', methods=['POST'])
def math_submit():
    """提交数学练习答案"""
    practice_id = request.form.get('practice_id', type=int)
    answers = session.get('answers', {})  # {id: correct_answer}
    
    if not practice_id or not answers:
        return redirect(url_for('math_practice'))
    
    # 收集用户答案（按题目ID顺序）
    user_answers = []
    for qid in sorted(answers.keys()):
        answer = request.form.get(f'answer_{qid}', type=int)
        user_answers.append(answer)
    
    # 提交并获取结果
    result = submit_practice(practice_id, user_answers)
    
    # 发送通知给家长
    send_practice_result(result)
    
    # 保存结果到 session（用于订正）- 只保存最小必要数据
    session['result'] = {
        'practice_id': result.get('practice_id'),
        'total': result.get('total'),
        'correct': result.get('correct'),
        'wrong': result.get('wrong'),
        'accuracy': result.get('accuracy'),
        'duration': result.get('duration'),
        'wrong_questions': result.get('wrong_questions', [])
    }
    
    return render_template('result.html', result=result)


@app.route('/math/correct', methods=['POST'])
def math_correct():
    """提交错题订正"""
    practice_id = request.form.get('practice_id', type=int)
    result = session.get('result', {})
    
    if not practice_id:
        return redirect(url_for('index'))
    
    # 收集订正答案
    corrections = {}
    wrong_questions = result.get('wrong_questions', [])
    
    for q in wrong_questions:
        answer = request.form.get(f'correction_{q["id"]}', type=int)
        if answer is not None:
            corrections[q['id']] = answer
    
    # 提交订正
    correction_result = submit_corrections(practice_id, corrections)
    
    if correction_result['all_correct']:
        # 全部订正正确，返回主页
        session.pop('result', None)
        session.pop('questions', None)
        return redirect(url_for('index'))
    else:
        # 还有错题，继续订正
        # 更新 result 中的 wrong_questions
        result['wrong_questions'] = correction_result['still_wrong']
        session['result'] = result
        return render_template('result.html', result=result)


@app.route('/history')
def history():
    """查看历史记录"""
    records = get_practice_history(30)
    return render_template('history.html', records=records)


@app.route('/api/math-stats')
def api_math_stats():
    """获取数学统计数据API"""
    days = request.args.get('days', 7, type=int)
    if days not in [7, 30]:
        days = 7
    stats = get_math_stats_for_chart(days)
    return jsonify(stats)


@app.route('/chinese')
def chinese_select():
    """语文阅读 - 选择内容类型"""
    return render_template('chinese_select.html',
                         reading_duration=config.READING_DURATION_MINUTES)


@app.route('/chinese/<content_type>')
def chinese_reading_type(content_type):
    """语文阅读页面 - 指定内容类型"""
    current_user = get_current_user()
    # 根据类型获取内容
    if content_type == 'local':
        # 本地经典故事
        from generators.stories import get_random_story as get_local_story
        story = get_local_story()
    else:
        # 从TianAPI获取
        try:
            from services.tianapi import fetch_tianapi_content
            story = fetch_tianapi_content(content_type)
            if story:
                story['id'] = 'api'
            else:
                # API失败，回退到本地
                from generators.stories import get_random_story as get_local_story
                story = get_local_story()
        except Exception as e:
            print(f"获取内容失败: {e}")
            from generators.stories import get_random_story as get_local_story
            story = get_local_story()
    
    # 创建阅读记录（关联当前用户）
    record_id = create_reading_record(story.get('id', 'unknown'), story['title'], user_name=current_user)
    
    # 只保存必要的 ID 到 session（避免 cookie 过大）
    session['reading_record_id'] = record_id
    session['content_type'] = content_type
    
    return render_template('chinese_reading.html', 
                         story=story, 
                         record_id=record_id,
                         content_type=content_type,
                         reading_duration=config.READING_DURATION_MINUTES,
                         current_user=current_user)


@app.route('/chinese/complete', methods=['POST'])
def chinese_complete():
    """完成阅读确认"""
    record_id = request.form.get('record_id', type=int)
    
    if not record_id:
        record_id = session.get('reading_record_id')
    
    if not record_id:
        return jsonify({'success': False, 'message': '无效的阅读记录'})
    
    # 完成阅读记录
    result = complete_reading(record_id)
    
    if result:
        # 发送通知给家长
        send_reading_result(result)
        
        # 清除 session
        session.pop('reading_record_id', None)
        
        return jsonify({
            'success': True, 
            'message': '阅读完成！',
            'result': result
        })
    else:
        return jsonify({'success': False, 'message': '记录不存在'})


@app.route('/chinese/next', methods=['POST'])
def chinese_next_story():
    """获取下一个故事"""
    content_type = request.form.get('content_type', 'local')
    story = None
    
    if content_type != 'local':
        # 从TianAPI获取
        try:
            from services.tianapi import fetch_tianapi_content
            story = fetch_tianapi_content(content_type, force_new=True)
            if story:
                story['id'] = 'api'
        except Exception as e:
            print(f"下一故事API调用失败: {e}")
            story = None
    
    # 如果API失败或选择本地，使用本地故事
    if not story:
        story = get_random_story([])
    
    return jsonify({
        'success': True,
        'story': {
            'id': story.get('id', 'unknown'),
            'title': story.get('title', '故事'),
            'image': story.get('image', '📖'),
            'content': story.get('content', '')
        }
    })


if __name__ == '__main__':
    print(f"""
╔══════════════════════════════════════════════════════════════╗
║                    📚 每日作业系统启动                        ║
╠══════════════════════════════════════════════════════════════╣
║  访问地址: http://{config.HOST}:{config.PORT}                          ║
║  iPad访问: http://<电脑IP>:{config.PORT}                          ║
║                                                              ║
║  提示: 请确保 iPad 和电脑在同一个 WiFi 网络下                 ║
╚══════════════════════════════════════════════════════════════╝
    """)
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
