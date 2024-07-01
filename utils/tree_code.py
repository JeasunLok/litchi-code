import numpy as np
import pandas as pd
import os
from read_table import read_table
from support import *

def find_all_U(string):
    indices = []
    index = string.find('U')
    while index != -1:
        indices.append(index)
        index = string.find('U', index + 1)
    return indices

def sunny_shady_identify(lists):
    sunny_list = []
    shady_list = []
    phenology = [row[7] for row in lists]
    unique_phenology = sorted(list(set(phenology)))
    if len(unique_phenology) == 1:
        for lst in lists:
            shady_list.append(lst)
            sunny_list.append(lst)
    elif len(unique_phenology) == 2:
        for lst in lists:
            if lst[7] == unique_phenology[0]:
                shady_list.append(lst)
            elif lst[7] == unique_phenology[1]:
                sunny_list.append(lst)
    elif len(unique_phenology) > 2:
        # 讨论点：三物候期->去掉  跳物候期->时序平滑
        top_two_phenology = unique_phenology[-2:]
        top_two_phenology_rows = [row for row in lists if row[7] in top_two_phenology]
        for lst in top_two_phenology_rows:
            if lst[7] == top_two_phenology[0]:
                shady_list.append(lst)
            elif lst[7] == top_two_phenology[1]:
                sunny_list.append(lst)
    return sunny_list, shady_list

def tree_warning_code(main_code, lists, main_index):
    first_activate_index = main_code.find("A")
    main_code_part1 = main_code[:first_activate_index].replace("0", "S")
    main_code_part2 = main_code[first_activate_index:]
    main_code = main_code_part1 + main_code_part2

    main_code_list = []
    for lst in lists:
        main_code_temp = initial_tree_phenology_code(lst, main_code, main_index)
        main_code_list.append(main_code_temp)
    
    # print(main_code_list)

    # 待完成：合并阳面或阴面所有照片的编码
    # tree_warning_code = merge_tree_single_angle_code(main_code_list)

    # =============  暂时
    code_length = len(main_code_list[0])
    tree_warning_code = [''] * code_length
    for col in range(code_length):  
        # 获取当前列的所有字符  
        column_chars = [row[col] for row in main_code_list]  
        # 找到ASCII码最大的字符  
        max_char = max(column_chars, key=ord)  
        # 添加到结果列表中  
        tree_warning_code[col] = max_char  

    tree_warning_code = ''.join(tree_warning_code)  
    # =============


    # print(tree_warning_code)
    return tree_warning_code

def tree_main_code(main_index, lists, main_code):
    sunny_shady_code = []   
    for angle_lists in lists:
        initial_main_code = main_code
        num_phenology_list = []
        for lst in angle_lists:
            num_phenology = lst[7]
            num_phenology_list.append(num_phenology)
        
        for phenology in num_phenology_list:
            initial_main_code = initial_main_code[:main_index[phenology]] + "A" + initial_main_code[main_index[phenology]+1:]
        
        sunny_shady_code.append(tree_warning_code(initial_main_code, angle_lists, main_index))

    # 待完成：合并阳面和阴面的代码
    last_tree_warning_code = merge_tree_two_angle_code(sunny_shady_code)

    # =============  暂时
    # last_tree_warning_code = sunny_shady_code
    # =============

    return last_tree_warning_code

def tree_code_from_table(file_path):
    # 读取表
    headers, rows = read_table(file_path)

    # 修改第一列的照片名字为飞巡时间
    headers[0] = "上次飞巡时间"
    for row in rows:
        row[0] = row[0].split("_")[1][:8]
        
    # 树体分区编号代码
    zone_code = rows[0][4]
    # 树体编号代码
    num_code = rows[0][6]
    # 初始是否失效代码
    activate_code = "Y" # "Y" "N"
    # 初始树类型代码
    type_code = "P" # "P" "C" "B" "N"
    # 飞巡任务状态
    task_status_code = "S"
    # 下次飞巡任务截止时间
    ddl_code = "YYYYMMDD"
    # 初始物候期编码
    main_code = ("U"+"0"*36)*3+("U"+"0"*9)*2+("U"+"0"*27)*1+("U"+"0"*18)*2+("U"+"0"*9)*1+("U"+"0"*18)*1

    # print(main_code)
    # 物候期编码
    main_index = find_all_U(main_code)
    # print(main_index)
    time_code = []
    # print(rows)

    time_code_dict = group_by_time(rows)
    # 时序数据的处理需要单独传进去一个列表，包含所有的时序预警的指标，按照时间去做筛选，预警，这样就不需要
    # print(time_code_dict)
    for time, items in time_code_dict.items():
        # 区分阴阳面
        sunny_shady_items = sunny_shady_identify(items)
        time_tree_main_code = tree_main_code(main_index, sunny_shady_items, main_code)
        # print(time_tree_main_code)
        time_code.append(str(zone_code).zfill(6)  + "-" + num_code + "-" + activate_code + "-" + type_code + "-" + task_status_code + "-" + str(time) + "-" + ddl_code + "-" + time_tree_main_code)
        
    return time_code

if __name__ == "__main__":
    # 测试示例
    file_path = r'data\ZSC-5295.xlsx'
    time_code = tree_code_from_table(file_path)

    for i in time_code:
        print(i)
