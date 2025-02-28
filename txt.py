import os
import re
from typing import *

def extract_dharani_title_and_roman(文本文件路径, 输出文本文件路径):
    """
    title: 文本陀罗尼标题和罗马拼音提取工具 (最终极改进版)
    description: 从文本文件中提取陀罗尼标题及其对应的罗马拼音，并保存到指定的输出文件中。
                 此版本彻底解决了各种标题格式问题，包括括号、卍字符、空格、数字、以及 "陀罗尼" 和 "陀罗尼卍" 结尾。
    inputs:
        - 文本文件路径 (file): 文本文件路径，eg: "D:/data/经文.txt"
        - 输出文本文件路径 (str): 输出文本文件路径，eg: "D:/data/提取陀罗尼_标题_罗马拼音.txt"
    outputs:
        - result (str): 处理结果信息，eg: "陀罗尼标题和罗马拼音已成功提取"
    """

    try:
        # 检查文件存在性
        if not os.path.exists(文本文件路径):
            return "错误：输入文件不存在"

        # 检查文件是否为文本文件
        if not 文本文件路径.lower().endswith(('.txt', '.text')):
            return "错误：输入文件不是文本格式 (建议 .txt 或 .text)"

        # 读取整个文件内容
        with open(文本文件路径, 'r', encoding='utf-8') as text_file:
            content = text_file.read()

        # 查找所有M开头的编号标记
        title_positions = []
        for match in re.finditer(r'M\d{2}\.\d{2}', content):
            title_positions.append(match.start())
        
        # 添加文件结束位置作为最后一个标题的结束位置
        title_positions.append(len(content))
        
        dharanis_data = {}
        
        # 处理每个标题块
        for i in range(len(title_positions) - 1):
            start_pos = title_positions[i]
            end_pos = title_positions[i+1]
            block_content = content[start_pos:end_pos]
            
            # 提取标题 - 查找从M开头到陀罗尼/真言结尾的部分
            title_match = re.search(r'M\d{2}\.\d{2}[\s\S]*?(?:陀罗尼|真言)(?:\s*\([^)]+\))*\s*卍?', block_content)
            if not title_match:
                # 如果没有找到标准格式的标题，尝试查找只有编号的标题
                title_match = re.search(r'M\d{2}\.\d{2}[^\n]*', block_content)
                if not title_match:
                    continue
            
            # 提取标题并清理
            title = title_match.group(0).replace('\n', ' ').strip()
            
            # 处理标题中的多余空格，确保标题连续
            title = re.sub(r'\s+', ' ', title)  # 将多个空格替换为单个空格
            # 特别处理标题中的关键词之间的空格，如"止 雨"变为"止雨"
            title = re.sub(r'([\u4e00-\u9fff])\s+([\u4e00-\u9fff])', r'\1\2', title)
            
            # 检查标题是否以"陀罗尼"或"真言"结尾
            if not re.search(r'(陀罗尼|真言)(?:\s*\([^)]+\))*\s*卍?$', title):
                # 检查标题是否包含"陀"字
                if '陀' in title and not re.search(r'陀罗尼', title):
                    # 如果包含"陀"字但不完整，补全为"陀罗尼"
                    title = re.sub(r'陀\s*$', '陀罗尼', title)
                # 如果标题末尾没有适当的结尾，添加"陀罗尼"
                if not re.search(r'(陀罗尼|真言)(?:\s*\([^)]+\))*\s*卍?$', title):
                    title += "陀罗尼"
            
            # 获取标题后的内容
            remaining_content = block_content[title_match.end():]
            
            # 处理罗马拼音行
            roman_words = []
            for line in remaining_content.split('\n'):
                line = line.strip()
                if not line:
                    continue
                    
                # 罗马拼音行检测：以字母开头，不包含中文，但可能包含数字和特殊字符
                if re.match(r'^[a-zA-Z]', line) and not re.search(r'[一-鿿]', line) and not line.startswith('——') and not line.startswith('卍'):
                    # 清理并规范化文本
                    cleaned_line = ' '.join(filter(None, line.split()))
                    # 移除数字（包括单独的数字和词后面的数字）
                    cleaned_line = re.sub(r'\s*\d+\s*', ' ', cleaned_line)
                    # 移除行末的单个字母（如L、R等标记）
                    cleaned_line = re.sub(r'\s+[A-Z]$', '', cleaned_line)
                    # 移除末尾的单个字母（无空格）
                    cleaned_line = re.sub(r'[A-Z]$', '', cleaned_line)
                    cleaned_line = cleaned_line.strip()
                    if cleaned_line:
                        roman_words.append(cleaned_line)
                # 增加对特殊字符开头但包含罗马拼音的行的处理
                elif re.search(r'[a-zA-Z]', line) and not re.search(r'[一-鿿]', line) and not line.startswith('——'):
                    # 提取行中的罗马拼音部分 - 扩展支持的特殊字符集
                    roman_part = re.sub(r'[^a-zA-ZāĀīĪūŪṛṚṝṜḷḶḹḸṃṂḥḤṅṄñÑṭṬḍḌṇṆśŚṣṢ\s]', ' ', line)
                    cleaned_line = ' '.join(filter(None, roman_part.split()))
                    # 移除数字（包括单独的数字和词后面的数字）
                    cleaned_line = re.sub(r'\s*\d+\s*', ' ', cleaned_line)
                    # 移除行末的单个字母（如L、R等标记）
                    cleaned_line = re.sub(r'\s+[A-Z]$', '', cleaned_line)
                    # 移除末尾的单个字母（无空格）
                    cleaned_line = re.sub(r'[A-Z]$', '', cleaned_line)
                    cleaned_line = cleaned_line.strip()
                    if cleaned_line:
                        roman_words.append(cleaned_line)
            
            # 保存陀罗尼数据
            if roman_words:
                dharanis_data[title] = " ".join(roman_words)

        # 创建输出目录（如果不存在）
        output_dir = os.path.dirname(输出文本文件路径)
        if output_dir and not os.path.exists(output_dir):
            os.makedirs(output_dir)

        # 写入输出文件
        with open(输出文本文件路径, 'w', encoding='utf-8') as output_file:
            for title, roman in dharanis_data.items():
                try:
                    output_file.write(f"{title}\n")
                    output_file.write(f"{roman}\n")
                    output_file.write("\n")
                except Exception as e:
                    print(f"处理失败: '{title}'")
                    print(f"错误详情: {str(e)}")
                    continue

        return f"文本文件中的陀罗尼标题和罗马拼音已成功提取到 {输出文本文件路径}"

    except Exception as e:
        print(f"处理过程中出现错误：{str(e)}")
        return f"处理失败：{str(e)}"


# 示例使用
if __name__ == '__main__':
    text_file_path = "1.txt"  # 替换为你的文本文件路径
    output_text_path = "提取陀罗尼_标题_罗马拼音_最终极版.txt"
    result_message = extract_dharani_title_and_roman(text_file_path, output_text_path)
    print(result_message)