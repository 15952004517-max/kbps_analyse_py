import os
import re
import pandas as pd
# test modigy 1645
def quick_parse_log_v3(log_path):
    """
    针对图片格式深度优化：提取时间戳，清洗掉Kbps单位，只保留纯数字
    """
    # 新正则表达式：
    # Group(1): 匹配类似 5.199.19 的时间标识
    # Group(2): 匹配 UL 后面的纯数字
    # Group(3): 匹配 ACK 后面的纯数字
    # Group(4): 匹配 NACK 后面的纯数字
    pattern = re.compile(
        r'(\d+\.\d+\.\d+).*?UL:\s*(\d+)\s*Kbps,\s*ACK\s*(\d+),\s*NACK\s*(\d+)', 
        re.IGNORECASE
    )
    
    data_list = []
    
    if not os.path.exists(log_path):
        print(f"❌ 错误：在当前目录下未找到文件 {log_path}")
        return data_list

    print(f"⚡ 开始快速解析: {log_path} ...")
    
    # 采用 1MB 缓存逐行读取
    with open(log_path, 'r', encoding='utf-8', errors='ignore', buffering=1024*1024) as f:
        for line_num, line in enumerate(f, 1):
            match = pattern.search(line)
            if match:
                time_stamp = match.group(1)       # 例如 "5.199.19"
                kbps_val = int(match.group(2))     # 转换为纯数字，例如 1435
                ack_val = int(match.group(3))      # 例如 479
                nack_val = int(match.group(4))     # 例如 17
                
                data_list.append({
                    'Line': line_num,
                    'Time_Stamp': time_stamp,
                    'UL_KBPS': kbps_val,
                    'UL_ACK': ack_val,
                    'UL_NACK': nack_val
                })
                
    return data_list


def export_to_excel(data, output_name='kbps_final_report.xlsx'):
    if not data:
        print("⚠️ 未匹配到任何符合条件的数据。")
        return
        
    print(f"📊 正在将 {len(data)} 条数据写入 Excel...")
    df = pd.DataFrame(data)
    
    # 调整列的顺序，让时间戳和行号靠前
    df = df[['Line', 'Time_Stamp', 'UL_KBPS', 'UL_ACK', 'UL_NACK']]
    
    # 导出为 Excel
    df.to_excel(output_name, index=False)
    print(f"🎉 成功！Excel 文件已保存至: {os.path.abspath(output_name)}")


if __name__ == '__main__':
    LOG_FILE = 'kbps.log'
    OUTPUT_FILE = 'kbps_final_report.xlsx'
    
    extracted_data = quick_parse_log_v3(LOG_FILE)
    export_to_excel(extracted_data, OUTPUT_FILE)
