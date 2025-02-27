import re
import os

def extract_roman_chant(input_path, output_path):
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件 {input_path} 不存在")

        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 使用正则表达式匹配每个咒语块
        pattern = r'M\d+\.\d+[^\n]*?(?:\n|$)[\s\S]*?(?=\nM\d+\.\d+|\Z)'
        chant_blocks = re.finditer(pattern, content)
        
        output = []
        for block in chant_blocks:
            block_text = block.group(0)
            
            # 提取标题
            title_match = re.search(r'M\d+\.\d+[^\n]*', block_text)
            if title_match:
                title = title_match.group(0).strip()
            else:
                continue
                
            # 提取罗马拼音部分（只包含拉丁字母、空格和特殊符号的行）
            roman_pattern = r'^[a-zA-Z\s\dāīūēōṛṝḷḹṅñṇṃḥṣśṭḍṅṇ\W]+$'
            lines = block_text.split('\n')
            roman_lines = []
            
            for line in lines:
                line = line.strip()
                if line and re.match(roman_pattern, line):
                    # 清理并规范化文本
                    cleaned_line = ' '.join(filter(None, line.split()))
                    if cleaned_line:
                        roman_lines.append(cleaned_line)
            
            if roman_lines:
                output.append(f"{title}\n{' '.join(roman_lines)}")

        # 确保输出目录存在
        os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
        
        # 写入输出文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n\n'.join(output))
            
        print(f"转换完成：已生成 {output_path}")
            
    except Exception as e:
        print(f"转换过程中出现错误：{str(e)}")
        raise

if __name__ == '__main__':
    input_file = 'd:\\audio\\1\\1.txt'
    output_file = 'd:\\audio\\1\\absolute\\path\\to\\output.txt'
    extract_roman_chant(input_file, output_file)