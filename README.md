# 陀罗尼提取工具

## 项目简介

这个项目提供了一套工具，用于从文本文件中提取陀罗尼标题及其对应的罗马拼音，并保存到指定的输出文件中。

## 主要功能

- 从文本文件中提取陀罗尼标题
- 提取对应的罗马拼音
- 处理各种标题格式，包括括号、卍字符、空格、数字等
- 支持"陀罗尼"和"陀罗尼卍"等多种结尾格式

## 文件说明

- `txt.py`: 主要的提取工具，包含提取陀罗尼标题和罗马拼音的功能
- `absolute/path/to/convert_chant.py`: 另一个转换工具，提供不同的提取方法
- `提取陀罗尼_标题_罗马拼音.txt`: 提取结果示例
- `提取陀罗尼_标题_罗马拼音_最终极版.txt`: 改进版提取结果示例

## 使用方法

```python
from txt import extract_dharani_title_and_roman

# 使用示例
text_file_path = "1.txt"  # 替换为你的文本文件路径
output_text_path = "提取陀罗尼_标题_罗马拼音_最终极版.txt"
result_message = extract_dharani_title_and_roman(text_file_path, output_text_path)
print(result_message)
```

## 注意事项

- 输入文件必须是文本格式（.txt或.text）
- 文本内容需要包含M开头的编号标记（如M01.01）
- 标题格式应符合特定模式，以便正确提取