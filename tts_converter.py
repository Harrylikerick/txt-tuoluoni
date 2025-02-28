import os
import re
import requests
import time
from gtts import gTTS
import urllib3
import socks
import socket
import random

# 禁用SSL警告
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def setup_proxy():
    """
    自动配置代理网络
    尝试多种常见代理配置方式
    """
    try:
        # 尝试使用系统代理
        print("正在尝试使用系统代理...")
        # 方法1: 使用环境变量设置HTTP代理
        os.environ['HTTP_PROXY'] = 'http://127.0.0.1:7890'
        os.environ['HTTPS_PROXY'] = 'http://127.0.0.1:7890'
        
        # 方法2: 使用SOCKS代理
        # 创建原始socket的引用
        original_socket = socket.socket
        
        # 尝试配置SOCKS5代理
        socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 7890)
        socket.socket = socks.socksocket
        
        # 测试代理连接
        try:
            test_response = requests.get("https://www.google.com", timeout=5, verify=False)
            if test_response.status_code == 200:
                print("代理配置成功！")
                return True
        except Exception as e:
            print(f"代理测试失败: {e}")
            # 恢复原始socket
            socket.socket = original_socket
            
            # 尝试其他常见代理端口
            common_ports = [1080, 8080, 8118, 10809]
            for port in common_ports:
                try:
                    print(f"尝试端口 {port}...")
                    os.environ['HTTP_PROXY'] = f'http://127.0.0.1:{port}'
                    os.environ['HTTPS_PROXY'] = f'http://127.0.0.1:{port}'
                    test_response = requests.get("https://www.google.com", timeout=5, verify=False)
                    if test_response.status_code == 200:
                        print(f"代理配置成功！使用端口: {port}")
                        return True
                except:
                    continue
        
        print("无法自动配置代理，请手动设置代理后重试")
        return False
    except Exception as e:
        print(f"代理配置过程中出现错误: {e}")
        return False

def extract_dharanis(file_path):
    """
    从文件中提取陀罗尼标题和罗马拼音
    返回字典 {标题: 罗马拼音}
    """
    dharanis = {}
    current_title = None
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # 按空行分割内容
        blocks = content.split('\n\n')
        
        for block in blocks:
            lines = block.strip().split('\n')
            if len(lines) >= 2:
                title = lines[0].strip()
                roman = lines[1].strip()
                
                # 确保标题是陀罗尼标题（以M开头）
                if title.startswith('M') and ('陀罗尼' in title or '真言' in title):
                    dharanis[title] = roman
    
    except Exception as e:
        print(f"提取陀罗尼时出错: {e}")
    
    return dharanis

def convert_to_audio(dharanis, output_dir='audio_files'):
    """
    将陀罗尼罗马拼音转换为罗马尼亚语音频
    """
    # 创建输出目录
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    success_count = 0
    failed_items = []
    
    for title, roman_text in dharanis.items():
        try:
            # 清理文件名
            safe_title = re.sub(r'[\\/:*?"<>|]', '_', title)
            output_file = os.path.join(output_dir, f"{safe_title}.mp3")
            
            print(f"正在转换: {title}")
            print(f"罗马拼音: {roman_text}")
            
            # 使用gTTS将文本转换为语音（使用罗马尼亚语）
            tts = gTTS(text=roman_text, lang='ro', slow=False)
            tts.save(output_file)
            
            print(f"已保存到: {output_file}")
            success_count += 1
            
            # 添加随机延迟，避免API限制
            time.sleep(random.uniform(1.0, 3.0))
            
        except Exception as e:
            print(f"转换失败 '{title}': {e}")
            failed_items.append((title, str(e)))
    
    return success_count, failed_items

def main():
    # 设置代理
    if not setup_proxy():
        print("警告: 代理设置失败，将尝试直接连接...")
    
    # 提取陀罗尼数据
    input_file = "提取陀罗尼_标题_罗马拼音_最终极版.txt"
    print(f"从 {input_file} 提取陀罗尼数据...")
    
    dharanis = extract_dharanis(input_file)
    print(f"共提取到 {len(dharanis)} 个陀罗尼")
    
    if not dharanis:
        print("未找到陀罗尼数据，请检查输入文件")
        return
    
    # 转换为音频
    output_dir = "dharani_audio"
    print(f"开始转换为罗马尼亚语音频，输出目录: {output_dir}")
    
    success_count, failed_items = convert_to_audio(dharanis, output_dir)
    
    # 输出结果统计
    print("\n转换完成!")
    print(f"成功: {success_count}/{len(dharanis)}")
    
    if failed_items:
        print(f"失败: {len(failed_items)}")
        print("失败项目:")
        for title, error in failed_items:
            print(f"  - {title}: {error}")

if __name__ == "__main__":
    main()