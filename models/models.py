# -*- coding: utf-8 -*-
"""数据库模型"""

import sqlite3
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
import json

import config


def get_current_time():
    """获取当前时区的时间"""
    utc_now = datetime.now(timezone.utc)
    local_time = utc_now + timedelta(hours=config.TIMEZONE_OFFSET_HOURS)
    return local_time


def get_db_connection():
    """获取数据库连接"""
    conn = sqlite3.connect(config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    """初始化数据库"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 创建练习记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS practice (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            subject TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            duration_seconds INTEGER,
            total_questions INTEGER,
            correct_count INTEGER,
            accuracy REAL,
            is_corrected INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # 创建题目记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS question (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            practice_id INTEGER NOT NULL,
            question_num INTEGER NOT NULL,
            num1 INTEGER NOT NULL,
            operator TEXT NOT NULL,
            num2 INTEGER NOT NULL,
            correct_answer INTEGER NOT NULL,
            user_answer INTEGER,
            is_correct INTEGER,
            corrected_answer INTEGER,
            is_corrected INTEGER DEFAULT 0,
            FOREIGN KEY (practice_id) REFERENCES practice (id)
        )
    ''')
    
    conn.commit()
    conn.close()


def create_practice(subject: str, questions: List[Dict]) -> int:
    """
    创建新的练习记录
    
    Args:
        subject: 学科
        questions: 题目列表
        
    Returns:
        practice_id
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now = get_current_time()
    date_str = now.strftime('%Y-%m-%d')
    start_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO practice (date, subject, start_time, total_questions)
        VALUES (?, ?, ?, ?)
    ''', (date_str, subject, start_time, len(questions)))
    
    practice_id = cursor.lastrowid
    
    # 保存题目
    for q in questions:
        cursor.execute('''
            INSERT INTO question (practice_id, question_num, num1, operator, num2, correct_answer)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (practice_id, q['id'], q['num1'], q['operator'], q['num2'], q['answer']))
    
    conn.commit()
    conn.close()
    
    return practice_id


def submit_practice(practice_id: int, user_answers: List[int]) -> Dict:
    """
    提交练习答案
    
    Args:
        practice_id: 练习ID
        user_answers: 用户答案列表
        
    Returns:
        练习结果
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取题目
    cursor.execute('''
        SELECT * FROM question WHERE practice_id = ? ORDER BY question_num
    ''', (practice_id,))
    questions = cursor.fetchall()
    
    correct_count = 0
    wrong_questions = []
    
    for i, q in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else None
        is_correct = 1 if user_answer == q['correct_answer'] else 0
        
        if is_correct:
            correct_count += 1
        else:
            wrong_questions.append({
                'id': q['question_num'],
                'display': f"{q['num1']} {q['operator']} {q['num2']} = ",
                'correct_answer': q['correct_answer'],
                'user_answer': user_answer
            })
        
        # 更新题目答案
        cursor.execute('''
            UPDATE question SET user_answer = ?, is_correct = ?
            WHERE practice_id = ? AND question_num = ?
        ''', (user_answer, is_correct, practice_id, q['question_num']))
    
    # 更新练习记录
    now = get_current_time()
    end_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('SELECT start_time FROM practice WHERE id = ?', (practice_id,))
    practice = cursor.fetchone()
    start = datetime.strptime(practice['start_time'], '%Y-%m-%d %H:%M:%S')
    duration = int((now - start).total_seconds())
    
    total = len(questions)
    accuracy = round(correct_count / total * 100, 1) if total > 0 else 0
    
    cursor.execute('''
        UPDATE practice SET end_time = ?, duration_seconds = ?, 
                           correct_count = ?, accuracy = ?
        WHERE id = ?
    ''', (end_time, duration, correct_count, accuracy, practice_id))
    
    conn.commit()
    conn.close()
    
    return {
        'practice_id': practice_id,
        'total': total,
        'correct': correct_count,
        'wrong': total - correct_count,
        'accuracy': accuracy,
        'duration_seconds': duration,
        'duration_display': format_duration(duration),
        'wrong_questions': wrong_questions
    }


def submit_corrections(practice_id: int, corrections: Dict[int, int]) -> Dict:
    """
    提交错题订正
    
    Args:
        practice_id: 练习ID
        corrections: 订正答案 {question_num: answer}
        
    Returns:
        订正结果
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    all_correct = True
    still_wrong = []
    
    for question_num, answer in corrections.items():
        cursor.execute('''
            SELECT * FROM question WHERE practice_id = ? AND question_num = ?
        ''', (practice_id, question_num))
        q = cursor.fetchone()
        
        if q and answer == q['correct_answer']:
            cursor.execute('''
                UPDATE question SET corrected_answer = ?, is_corrected = 1
                WHERE practice_id = ? AND question_num = ?
            ''', (answer, practice_id, question_num))
        else:
            all_correct = False
            if q:
                still_wrong.append({
                    'id': question_num,
                    'display': f"{q['num1']} {q['operator']} {q['num2']} = ",
                    'correct_answer': q['correct_answer'],
                    'user_answer': answer
                })
    
    if all_correct:
        cursor.execute('''
            UPDATE practice SET is_corrected = 1 WHERE id = ?
        ''', (practice_id,))
    
    conn.commit()
    conn.close()
    
    return {
        'all_correct': all_correct,
        'still_wrong': still_wrong
    }


def get_practice_history(limit: int = 30) -> List[Dict]:
    """获取练习历史（只返回已完成的记录）"""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT * FROM practice 
        WHERE accuracy IS NOT NULL 
        ORDER BY created_at DESC LIMIT ?
    ''', (limit,))
    
    practices = []
    for row in cursor.fetchall():
        # 从 start_time 获取完整的日期时间
        start_time = row['start_time']
        if start_time:
            try:
                dt = datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                date_display = dt.strftime('%Y-%m-%d %H:%M')
            except:
                date_display = row['date']
        else:
            date_display = row['date']
        
        practices.append({
            'id': row['id'],
            'date': date_display,
            'subject': row['subject'],
            'duration': format_duration(row['duration_seconds']) if row['duration_seconds'] else '-',
            'total': row['total_questions'],
            'correct': row['correct_count'],
            'accuracy': row['accuracy'],
            'is_corrected': row['is_corrected']
        })
    
    conn.close()
    return practices


def format_duration(seconds: int) -> str:
    """格式化时间显示"""
    if seconds is None:
        return '-'
    minutes = seconds // 60
    secs = seconds % 60
    if minutes > 0:
        return f"{minutes}分{secs}秒"
    return f"{secs}秒"


# 初始化数据库
init_db()
