import re  
import os  
from pypinyin import pinyin, Style  
from tqdm import tqdm  
  
# 读取原始文件，处理并写入对应的txt文件  
def process_file(input_file, output_file):  
    with open(input_file, 'r', encoding='utf-8') as f_in, \
         open(output_file, 'w', encoding='utf-8') as f_out:  
          
        lines = f_in.readlines()  
        for line in tqdm(lines, desc=f"Processing {input_file}", unit="line"):  
            line = line.strip()  # 去除行尾换行符和首尾的空白  
            if not line or line.startswith('#'):  # 跳过空白行或以#开头的行  
                continue  
              
            # 检查行中是否包含[a-z]  
            if re.search(r'[a-z]', line):  
                f_out.write(line + '\n')  # 如果包含[a-z]，则直接写入  
                continue  
              
            # 以\t切分  
            parts = line.split('\t')  
            if parts:  
                # 对切分后的列表第一项去除首尾空白，并标注汉语拼音  
                first_part = parts[0].strip()  
                pinyin_list = pinyin(first_part, style=Style.NORMAL)  
                pinyin_str = ' '.join(p[0] for p in pinyin_list)  
                  
                # 拼接新的字符串，并写入对应的txt文件  
                output_line = f"{first_part}\t{pinyin_str}"  
                if len(parts) > 1:  
                    output_line += f"\t{parts[1].strip()}"  # 也去除第二部分首尾的空白  
                if len(parts) > 2:  
                    output_line += f"\t{parts[2].strip()}"  # 去除第三部分首尾的空白  
                f_out.write(output_line + '\n')  
  
# 遍历当前目录下所有的.yaml文件，并一一处理  
def process_all_yaml_files():  
    current_directory = os.getcwd()  # 获取当前工作目录  
    for filename in os.listdir(current_directory):  
        if filename.endswith('.yaml'):  
            input_file = os.path.join(current_directory, filename)  
            output_file = os.path.splitext(input_file)[0] + '.txt'  # 替换.yaml为.txt  
            process_file(input_file, output_file)  
  
# 调用函数处理所有文件  
process_all_yaml_files()