# -*- coding: utf-8 -*-
"""
学生每日扩展作业 - Flask 主应用
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import json

import config
from generators.math_generator import generate_questions
from models.models import (
    create_practice, submit_practice, submit_corrections,
    get_practice_history
)
from services.notify import send_practice_result

app = Flask(__name__)
app.secret_key = config.SECRET_KEY


@app.route('/')
def index():
    """主页 - 学科分类"""
    history = get_practice_history(5)
    return render_template('index.html', history=history)


@app.route('/math')
def math_practice():
    """数学练习页面"""
    # 生成题目
    questions = generate_questions(
        count=config.MATH_QUESTION_COUNT,
        max_number=config.MATH_MAX_NUMBER
    )
    
    # 创建练习记录
    practice_id = create_practice('数学', questions)
    
    # 保存题目到 session
    session['questions'] = questions
    session['practice_id'] = practice_id
    
    return render_template('math_practice.html', 
                         questions=questions, 
                         practice_id=practice_id)


@app.route('/math/submit', methods=['POST'])
def math_submit():
    """提交数学练习答案"""
    practice_id = request.form.get('practice_id', type=int)
    questions = session.get('questions', [])
    
    if not practice_id or not questions:
        return redirect(url_for('math_practice'))
    
    # 收集用户答案
    user_answers = []
    for q in questions:
        answer = request.form.get(f'answer_{q["id"]}', type=int)
        user_answers.append(answer)
    
    # 提交并获取结果
    result = submit_practice(practice_id, user_answers)
    
    # 发送通知给家长
    send_practice_result(result)
    
    # 保存结果到 session（用于订正）
    session['result'] = result
    
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
