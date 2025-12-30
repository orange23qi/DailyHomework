# -*- coding: utf-8 -*-
"""天行数据API服务 + 拼音转换"""

import requests
import re
import time
import random
import config

try:
    from pypinyin import pinyin, Style
    PYPINYIN_AVAILABLE = True
except ImportError:
    PYPINYIN_AVAILABLE = False
    print("警告: pypinyin未安装，将使用本地故事")

# 简单的内存缓存：每种类型缓存多条内容，避免频繁调用API
_content_cache = {}  # {content_type: [content1, content2, ...]}
_cache_size = 10  # 每种类型最多缓存10条
_last_api_call = 0  # 上次API调用时间
_api_cooldown = 2  # API调用间隔（秒）


def add_pinyin_to_text(text):
    """
    将纯中文文本转换为带拼音的HTML
    
    Args:
        text: 纯中文文本
        
    Returns:
        带<ruby>标签的HTML字符串
    """
    if not PYPINYIN_AVAILABLE:
        return f"<p>{text}</p>"
    
    result = []
    # 按段落分割
    paragraphs = text.strip().split('\n')
    
    for para in paragraphs:
        if not para.strip():
            continue
            
        para_html = []
        for char in para:
            if '\u4e00' <= char <= '\u9fff':  # 是汉字
                py = pinyin(char, style=Style.TONE)[0][0]
                para_html.append(f'<ruby>{char}<rt>{py}</rt></ruby>')
            else:
                para_html.append(char)
        
        result.append(f'<p>{"".join(para_html)}</p>')
    
    return '\n'.join(result)


def fetch_tianapi_content(content_type='fairytales', force_new=False):
    """
    从天行数据API获取内容（带缓存）
    
    Args:
        content_type: 内容类型 (fairytales/story/riddle/rkl/naowan)
        force_new: 是否强制获取新内容（跳过缓存）
        
    Returns:
        dict: {title, content, image, type_name} 或 None
    """
    global _content_cache, _last_api_call
    
    if config.TIANAPI_KEY == 'YOUR_TIANAPI_KEY':
        return None
    
    # 优先从缓存获取（除非强制获取新内容）
    if not force_new and content_type in _content_cache and _content_cache[content_type]:
        cached = _content_cache[content_type]
        item = random.choice(cached)
        print(f"从缓存获取({content_type}): {item.get('title', '')}")
        return item
    
    # 检查API调用频率限制
    now = time.time()
    if now - _last_api_call < _api_cooldown:
        print(f"API调用过于频繁，等待冷却...")
        # 如果缓存中有多个故事，尝试返回一个不同的
        if content_type in _content_cache and len(_content_cache[content_type]) > 1:
            item = random.choice(_content_cache[content_type])
            print(f"冷却期间从缓存获取({content_type}): {item.get('title', '')}")
            return item
        return None
    
    _last_api_call = now
    print(f"正在调用TianAPI获取新故事({content_type})...")
    
    # fairytales API需要id参数，改用story API的type=3
    actual_type = content_type
    if content_type == 'fairytales':
        actual_type = 'story'
    
    url = f"https://apis.tianapi.com/{actual_type}/index"
    
    # 不同API需要不同参数
    # 使用随机page来获取不同的故事（API每30秒才更新一次，所以需要翻页）
    random_page = random.randint(1, 50)  # 随机选择1-50页
    params = {'key': config.TIANAPI_KEY, 'num': 1, 'page': random_page}
    
    # story API可以通过type区分故事类型
    if content_type == 'fairytales':
        params['type'] = 3  # 童话故事
    elif content_type == 'story':
        params['type'] = 4  # 寓言故事
    elif content_type == 'chengyu':
        # 成语典故API需要word参数（必需）
        common_idioms = [
            '马到成功', '一马当先', '画龙点睛', '守株待兔', '掩耳盗铃',
            '叶公好龙', '狐假虎威', '刻舟求剑', '亡羊补牢', '拔苗助长',
            '井底之蛙', '杯弓蛇影', '对牛弹琴', '鹤立鸡群', '胸有成竹',
            '望梅止渴', '负荆请罪', '卧薪尝胆', '老马识途', '塞翁失马',
            '班门弄斧', '铁杵成针', '三顾茅庐', '纸上谈兵', '愚公移山',
            '精卫填海', '夸父追日', '后羿射日', '女娲补天', '盘古开天',
            '完璧归赵', '负荆请罪', '将相和', '闻鸡起舞', '程门立雪',
            '孔融让梨', '凿壁偷光', '囊萤映雪', '悬梁刺股', '韦编三绝'
        ]
        params['word'] = random.choice(common_idioms)
        params.pop('page', None)  # 成语API不需要page参数
    
    print(f"API请求参数: page={random_page}, type={params.get('type', '不指定')}")
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if data.get('code') != 200:
            print(f"TianAPI错误({content_type}): {data.get('msg')}")
            return None
        
        # 处理返回数据（可能是dict或list，或者在result.list中）
        result = data.get('result', {})
        
        # 有些API返回的是 {"list": [...]}
        if isinstance(result, dict) and 'list' in result:
            result_list = result.get('list', [])
            if result_list and len(result_list) > 0:
                result = result_list[0]
        elif isinstance(result, list) and len(result) > 0:
            result = result[0]
        
        # 调试：打印返回的数据结构
        print(f"TianAPI解析后({content_type}): {result}")
        
        # 不同接口返回格式处理
        if content_type == 'riddle':
            title = "谜语"
            quest = result.get('quest', '') or result.get('question', '')
            answer = result.get('answer', '') or result.get('result', '')
            content = f"谜面：{quest}\n\n（想一想再看答案哦！）\n\n谜底：{answer}"
            image = "🤔"
        elif content_type == 'rkl':
            title = "绕口令"
            content = result.get('content', '') or result.get('list', '')
            image = "👅"
        elif content_type == 'naowan':
            title = "脑筋急转弯"
            # 尝试多种可能的字段名
            quest = result.get('quest', '') or result.get('question', '') or result.get('title', '')
            answer = result.get('answer', '') or result.get('result', '')
            content = f"问：{quest}\n\n（想一想再看答案哦！）\n\n答：{answer}"
            image = "💡"
        elif content_type == 'tenwhy':
            # 十万个为什么
            title = result.get('title', '十万个为什么')
            content = result.get('content', '')
            image = "❓"
        elif content_type == 'chengyu':
            # 成语典故
            chengyu = result.get('chengyu', '')
            pinyin = result.get('pinyin', '')
            diangu = result.get('diangu', '')  # 释义
            chuchu = result.get('chuchu', '')  # 出处
            fanli = result.get('fanli', '')    # 例句
            title = f"成语：{chengyu}"
            content = f"【拼音】{pinyin}\n\n【释义】{diangu}\n\n【出处】{chuchu}"
            if fanli:
                content += f"\n\n【例句】{fanli}"
            image = "📜"
        elif content_type == 'poetries':
            # 唐诗大全
            title = result.get('title', '唐诗')
            author = result.get('author', '')
            poem_content = result.get('content', '')
            content = f"【{author}】\n\n{poem_content}"
            image = "🏛️"
        elif content_type == 'poetry':
            # 唐诗三百首（带赏析）
            title = result.get('title', '唐诗')
            author = result.get('author', '')
            kind = result.get('kind', '')  # 诗体类型
            poem_content = result.get('content', '')
            intro = result.get('intro', '')  # 赏析
            content = f"【{author}】"
            if kind:
                content += f" / {kind}"
            content += f"\n\n{poem_content}"
            if intro:
                content += f"\n\n【赏析】\n{intro}"
            image = "🌸"
        else:
            title = result.get('title', '故事')
            content = result.get('content', '')
            image = "📖"
        
        if not content:
            return None
        
        # 添加拼音
        content_with_pinyin = add_pinyin_to_text(content)
        
        result_item = {
            'title': title,
            'content': content_with_pinyin,
            'image': image,
            'type_name': config.TIANAPI_CONTENT_TYPES.get(content_type, '故事')
        }
        
        # 添加到缓存
        if content_type not in _content_cache:
            _content_cache[content_type] = []
        _content_cache[content_type].append(result_item)
        # 限制缓存大小
        if len(_content_cache[content_type]) > _cache_size:
            _content_cache[content_type].pop(0)
        
        return result_item
        
    except Exception as e:
        print(f"TianAPI请求异常({content_type}): {e}")
        return None


def get_random_tianapi_content():
    """随机获取一种类型的内容"""
    import random
    content_types = list(config.TIANAPI_CONTENT_TYPES.keys())
    random.shuffle(content_types)
    
    for ct in content_types:
        result = fetch_tianapi_content(ct)
        if result:
            return result
    
    return None


if __name__ == '__main__':
    # 测试拼音转换
    test_text = "小蝌蚪在池塘里游来游去。"
    print(add_pinyin_to_text(test_text))
