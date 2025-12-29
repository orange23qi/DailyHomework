# -*- coding: utf-8 -*-
"""数学题目生成器"""

import random
from typing import List, Dict


def generate_questions(count: int = 20, max_number: int = 100) -> List[Dict]:
    """
    生成100以内的加减法题目
    
    Args:
        count: 题目数量
        max_number: 数字范围上限
        
    Returns:
        题目列表，每个题目包含 id, num1, operator, num2, answer
    """
    questions = []
    used_questions = set()  # 用于避免重复题目
    
    while len(questions) < count:
        operator = random.choice(['+', '-'])
        
        if operator == '+':
            # 加法：确保结果不超过 max_number
            num1 = random.randint(0, max_number)
            num2 = random.randint(0, max_number - num1)
            answer = num1 + num2
        else:
            # 减法：确保结果不为负数
            num1 = random.randint(0, max_number)
            num2 = random.randint(0, num1)
            answer = num1 - num2
        
        # 创建题目标识，用于去重
        question_key = f"{num1}{operator}{num2}"
        
        if question_key not in used_questions:
            used_questions.add(question_key)
            questions.append({
                'id': len(questions) + 1,
                'num1': num1,
                'operator': operator,
                'num2': num2,
                'answer': answer,
                'display': f"{num1} {operator} {num2} = "
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
