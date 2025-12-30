# -*- coding: utf-8 -*-
"""数学题目生成器"""

import random
from typing import List, Dict


def generate_questions(count: int = 20, max_number: int = 100) -> List[Dict]:
    """
    生成100以内的加减法题目
    
    题型包括：
    1. 普通题：a + b = ? 或 a - b = ?
    2. 填空题（第一个数未知）：□ + b = c 或 □ - b = c
    3. 填空题（第二个数未知）：a + □ = c 或 a - □ = c
    
    Args:
        count: 题目数量
        max_number: 数字范围上限
        
    Returns:
        题目列表，每个题目包含 id, num1, operator, num2, answer, display, question_type
    """
    questions = []
    used_questions = set()  # 用于避免重复题目
    
    # 题型：normal=普通题, blank_first=第一个数填空, blank_second=第二个数填空
    question_types = ['normal', 'normal', 'blank_first', 'blank_second']  # 普通题概率更高
    
    while len(questions) < count:
        question_type = random.choice(question_types)
        operator = random.choice(['+', '-'])
        
        if operator == '+':
            # 加法：确保结果不超过 max_number
            num1 = random.randint(1, max_number - 1)
            num2 = random.randint(1, max_number - num1)
            result = num1 + num2
        else:
            # 减法：确保结果不为负数
            num1 = random.randint(1, max_number)
            num2 = random.randint(1, num1)
            result = num1 - num2
        
        # 根据题型生成显示和答案
        if question_type == 'normal':
            # 普通题：a + b = ?
            display = f"{num1} {operator} {num2} = "
            answer = result
            question_key = f"normal_{num1}{operator}{num2}"
        elif question_type == 'blank_first':
            # 第一个数填空：□ + b = c
            display = f"□ {operator} {num2} = {result}"
            answer = num1
            question_key = f"blank1_{operator}{num2}={result}"
        else:  # blank_second
            # 第二个数填空：a + □ = c
            display = f"{num1} {operator} □ = {result}"
            answer = num2
            question_key = f"blank2_{num1}{operator}={result}"
        
        if question_key not in used_questions:
            used_questions.add(question_key)
            questions.append({
                'id': len(questions) + 1,
                'num1': num1,
                'operator': operator,
                'num2': num2,
                'answer': answer,
                'display': display,
                'question_type': question_type,
                'result': result  # 保存计算结果，用于前端显示
            })
    
    return questions


def check_answers(questions: List[Dict], user_answers: List[int]) -> Dict:
    """
    检查答案
    
    Args:
        questions: 题目列表
        user_answers: 用户答案列表
        
    Returns:
        包含正确数、错误数、正确率和错题列表的字典
    """
    correct_count = 0
    wrong_questions = []
    
    for i, question in enumerate(questions):
        user_answer = user_answers[i] if i < len(user_answers) else None
        
        if user_answer == question['answer']:
            correct_count += 1
        else:
            wrong_questions.append({
                'id': question['id'],
                'display': question['display'],
                'correct_answer': question['answer'],
                'user_answer': user_answer
            })
    
    total = len(questions)
    accuracy = (correct_count / total * 100) if total > 0 else 0
    
    return {
        'total': total,
        'correct': correct_count,
        'wrong': total - correct_count,
        'accuracy': round(accuracy, 1),
        'wrong_questions': wrong_questions
    }


if __name__ == '__main__':
    # 测试
    questions = generate_questions(5)
    for q in questions:
        print(f"{q['display']} (答案: {q['answer']})")
