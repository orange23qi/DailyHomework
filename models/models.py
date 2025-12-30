# -*- coding: utf-8 -*-
"""数据库模型"""

import sqlite3
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
import json

import config


def get_current_time():
    """获取当前时区的时间（返回无时区datetime）"""
    utc_now = datetime.utcnow()
    local_time = utc_now + timedelta(hours=config.TIMEZONE_OFFSET_HOURS)
    return local_time


def get_db_connection():
    """获取数据库连接（带并发优化）"""
    conn = sqlite3.connect(
        config.DATABASE_PATH,
        timeout=30.0,  # 遇到锁时等待最多30秒
        check_same_thread=False  # 允许多线程使用同一连接
    )
    conn.row_factory = sqlite3.Row
    
    # 启用 WAL 模式（Write-Ahead Logging）
    # WAL 模式允许读写并发，大幅减少锁冲突
    conn.execute('PRAGMA journal_mode=WAL')
    
    # 设置 busy_timeout（毫秒），遇到锁时重试等待
    conn.execute('PRAGMA busy_timeout=30000')
    
    # 启用外键约束
    conn.execute('PRAGMA foreign_keys=ON')
    
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
    
    # 创建阅读记录表
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reading_record (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            story_id INTEGER NOT NULL,
            story_title TEXT NOT NULL,
            start_time TEXT NOT NULL,
            end_time TEXT,
            duration_seconds INTEGER,
            completed INTEGER DEFAULT 0,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
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


def get_practice_history_by_days(days: int = 7) -> List[Dict]:
    """
    获取最近N天的练习记录（包括数学和语文）
    
    Args:
        days: 天数
        
    Returns:
        练习记录列表
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 计算起始日期
    now = get_current_time()
    start_date = (now - timedelta(days=days)).strftime('%Y-%m-%d')
    
    # 获取数学练习记录（只获取已完成的，即 accuracy 不为空的）
    cursor.execute('''
        SELECT p.*, 
               (SELECT COUNT(*) FROM question WHERE practice_id = p.id) as total_questions
        FROM practice p
        WHERE p.date >= ? AND p.accuracy IS NOT NULL
        ORDER BY p.start_time DESC
    ''', (start_date,))
    
    practices = []
    for row in cursor.fetchall():
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
            'start_time': start_time,
            'subject': row['subject'],
            'duration': format_duration(row['duration_seconds']) if row['duration_seconds'] else '-',
            'total': row['total_questions'],
            'correct': row['correct_count'],
            'accuracy': row['accuracy'],
            'is_corrected': row['is_corrected']
        })
    
    # 获取语文阅读记录
    cursor.execute('''
        SELECT * FROM reading_record
        WHERE date >= ? AND completed = 1
        ORDER BY start_time DESC
    ''', (start_date,))
    
    for row in cursor.fetchall():
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
            'id': f"reading_{row['id']}",
            'date': date_display,
            'start_time': start_time,
            'subject': '语文',
            'duration': format_duration(row['duration_seconds']) if row['duration_seconds'] else '-',
            'total': None,
            'correct': None,
            'accuracy': None,
            'is_corrected': None
        })
    
    # 按时间排序
    practices.sort(key=lambda x: x.get('start_time', ''), reverse=True)
    
    conn.close()
    return practices


def get_math_stats_for_chart(days: int = 7) -> Dict:
    """
    获取数学统计数据用于图表显示
    
    Args:
        days: 天数
        
    Returns:
        {labels: [], accuracy: [], duration: []}
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now = get_current_time()
    start_date = (now - timedelta(days=days)).strftime('%Y-%m-%d')
    
    cursor.execute('''
        SELECT date, AVG(accuracy) as avg_accuracy, AVG(duration_seconds) as avg_duration
        FROM practice
        WHERE subject = '数学' AND date >= ? AND accuracy IS NOT NULL
        GROUP BY date
        ORDER BY date ASC
    ''', (start_date,))
    
    labels = []
    accuracy = []
    duration = []
    
    for row in cursor.fetchall():
        labels.append(row['date'][5:])  # 只显示 MM-DD
        accuracy.append(round(row['avg_accuracy'], 1) if row['avg_accuracy'] else 0)
        duration.append(round(row['avg_duration'] / 60, 1) if row['avg_duration'] else 0)  # 转换为分钟
    
    conn.close()
    
    return {
        'labels': labels,
        'accuracy': accuracy,
        'duration': duration
    }


def create_reading_record(story_id: int, story_title: str) -> int:
    """
    创建阅读记录
    
    Args:
        story_id: 故事ID
        story_title: 故事标题
        
    Returns:
        record_id
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    now = get_current_time()
    date_str = now.strftime('%Y-%m-%d')
    start_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    cursor.execute('''
        INSERT INTO reading_record (date, story_id, story_title, start_time)
        VALUES (?, ?, ?, ?)
    ''', (date_str, story_id, story_title, start_time))
    
    record_id = cursor.lastrowid
    
    conn.commit()
    conn.close()
    
    return record_id


def complete_reading(record_id: int) -> Dict:
    """
    完成阅读记录
    
    Args:
        record_id: 阅读记录ID
        
    Returns:
        阅读结果
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 获取记录
    cursor.execute('SELECT * FROM reading_record WHERE id = ?', (record_id,))
    record = cursor.fetchone()
    
    if not record:
        conn.close()
        return None
    
    now = get_current_time()
    end_time = now.strftime('%Y-%m-%d %H:%M:%S')
    
    start = datetime.strptime(record['start_time'], '%Y-%m-%d %H:%M:%S')
    duration = int((now - start).total_seconds())
    
    cursor.execute('''
        UPDATE reading_record SET end_time = ?, duration_seconds = ?, completed = 1
        WHERE id = ?
    ''', (end_time, duration, record_id))
    
    conn.commit()
    conn.close()
    
    return {
        'record_id': record_id,
        'story_title': record['story_title'],
        'duration_seconds': duration,
        'duration_display': format_duration(duration),
        'date': record['date']
    }


# 初始化数据库
init_db()
