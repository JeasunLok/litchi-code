from tree_code import *
from collections import Counter

def phenology_num2code(phenology_num):
    phenology_mapping = {
        0: 'A',
        1: 'B',
        2: 'C',
        3: 'L',
        4: 'W',
        5: 'F',
        6: 'H',
        7: 'X',
        8: 'P',
        9: 'G'
    }
    return phenology_mapping[phenology_num]

def calculate_phenology_proportions(lst: list) -> list:
    count = Counter(lst)  
    total = len(lst)
    proportions = {key: value / total for key, value in count.items()}
    phenology_zone_string = ''.join(f'{key}{round(value * 10)}' for key, value in proportions.items())
    return phenology_zone_string

def calculate_grow_warning_proportions(lst: list) -> list:
    num = len(lst)
    G0_grow_warning_count = 0
    G_grow_warning_count = 0
    total_G_grow_warning_count = 0
    for s in lst:
        G0_grow_warning_count = G0_grow_warning_count + s.count('G0')
        total_G_grow_warning_count = total_G_grow_warning_count + s.count('G')

    G_grow_warning_count =  total_G_grow_warning_count - G0_grow_warning_count
    G0_grow_warning_ratio = G0_grow_warning_count/num
    G_grow_warning_ratio = G_grow_warning_count/num

    # 如果没有G和GO或者全是G0，只给GA等级
    # 如果不全是G0，且G比例大于20%小于50%给GB等级
    # 如果不全是G0，且G比例大于50%给GC等级

    if G0_grow_warning_ratio == 0 and G_grow_warning_ratio == 0:
        grow_warning_zone_string = "00"
    elif  G0_grow_warning_ratio > 0 and G_grow_warning_ratio < 0.2 and G_grow_warning_ratio >= 0:
        grow_warning_zone_string = "GA"
    elif  G0_grow_warning_ratio == 0 and G_grow_warning_ratio < 0.2 and G_grow_warning_ratio > 0:
        grow_warning_zone_string = "GA"
    elif  G0_grow_warning_ratio >= 0 and G_grow_warning_ratio >= 0.2 and G_grow_warning_ratio < 0.5:
        grow_warning_zone_string = "GB"
    elif  G0_grow_warning_ratio >= 0 and G_grow_warning_ratio >= 0.5:
        grow_warning_zone_string = "GC"
    
    return grow_warning_zone_string

def calculate_disease_warning_proportions(lst: list) -> list:
    num = len(lst)
    D0_disease_warning_count = 0
    D_disease_warning_count = 0
    total_D_disease_warning_count = 0
    for s in lst:
        D0_disease_warning_count = D0_disease_warning_count + s.count('D0')
        total_D_disease_warning_count = total_D_disease_warning_count + s.count('D')

    D_disease_warning_count =  total_D_disease_warning_count - D0_disease_warning_count
    D0_disease_warning_ratio = D0_disease_warning_count/num
    D_disease_warning_ratio = D_disease_warning_count/num

    # 如果没有D和DO或者全是D0，只给DA等级
    # 如果不全是D0，且D比例大于20%小于50%给DB等级
    # 如果不全是D0，且D比例大于50%给DC等级

    if D0_disease_warning_ratio == 0 and D_disease_warning_ratio == 0:
        disease_warning_zone_string = "00"
    elif  D0_disease_warning_ratio > 0 and D_disease_warning_ratio < 0.2 and D_disease_warning_ratio >= 0:
        disease_warning_zone_string = "DA"
    elif  D0_disease_warning_ratio == 0 and D_disease_warning_ratio < 0.2 and D_disease_warning_ratio > 0:
        disease_warning_zone_string = "DA"
    elif  D0_disease_warning_ratio >= 0 and D_disease_warning_ratio >= 0.2 and D_disease_warning_ratio < 0.5:
        disease_warning_zone_string = "DB"
    elif  D0_disease_warning_ratio >= 0 and D_disease_warning_ratio >= 0.5:
        disease_warning_zone_string = "DC"
    
    return disease_warning_zone_string

def index_A_information(index_A_first, index_A_second, tree_main_code):
    information = []
    # [0, 37, 74, 111, 121, 131, 159, 178, 197, 207]
    phenology_num_list = [0, 37, 74, 111, 121, 131, 159, 178, 197, 207]
    phenology_num_first = phenology_num_list.index(index_A_first)
    phenology_num_second = phenology_num_list.index(index_A_second)
    phenology_code_first = phenology_num2code(phenology_num_first)
    phenology_code_second = phenology_num2code(phenology_num_second)

    if index_A_second == -1:
        A_index = index_A_first
    else:
        A_index = index_A_second

    U_index = tree_main_code.find('U', A_index)
    if U_index == -1:
        U_index = len(tree_main_code)
    information_code = tree_main_code[index_A_first:U_index]
    print(information_code)
    information_split_code = [information_code[i:i+4] for i in range(0, len(information_code), 4)]

    phenology_num_subset = 1
    for information_split_code_subset in information_split_code:
        if information_split_code_subset == "000000000":
            phenology_num_subset = phenology_num_subset + 1
        else:
            phenology_code_subset = information_split_code_subset
            break
    
    information.append(phenology_code_first + str(phenology_num_subset))
    information.append(phenology_code_subset[:2])
    information.append(phenology_code_subset[2:])
    # print(information)
    return information

def orginal_zone_code_from_tree_code(tree_code_list):
    phenology_stats = []
    grow_warning_stats = []
    disease_warning_stats = []
    flight_time = ""

    for tree_code in tree_code_list:
        tree_split_code = tree_code.split("-")
        tree_zone_id_code = tree_split_code[0]
        tree_id_code = tree_split_code[1]
        tree_activated_code = tree_split_code[2]
        tree_mark_code = tree_split_code[3][0]
        tree_time_code = tree_split_code[3][1:]
        tree_main_code = tree_split_code[-1]

        # 简单的判断，先锋树的飞巡时间作为区域飞巡时间
        if tree_mark_code == "P":
            flight_time = tree_time_code
        
        index_A_first = tree_main_code.find("A")
        index_A_second = tree_main_code.find("A", index_A_first+1)
        phenology_stats.append(index_A_information(index_A_first, index_A_second, tree_main_code)[0])
        grow_warning_stats.append(index_A_information(index_A_first, index_A_second, tree_main_code)[1])
        disease_warning_stats.append(index_A_information(index_A_first, index_A_second, tree_main_code)[2])
        break
    

    phenology_zone_string = calculate_phenology_proportions(phenology_stats)
    grow_warning_zone_string = calculate_grow_warning_proportions(grow_warning_stats)
    disease_warning_zone_string = calculate_disease_warning_proportions(disease_warning_stats)

    zone_code = "-".join([phenology_zone_string, grow_warning_zone_string + disease_warning_zone_string, flight_time])

    return zone_code

if __name__ == "__main__":
    # 测试示例
    list = [
        "ZZZZZZZ-ws0y1met2cpq-Y-P20240130-USSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSUSSSSSSSSSA000000000000000000000000000A000000000000000000U000000000000000000U000000000U000000000000000000",
        "ZZZZZZZ-ws0y1mttfcpq-Y-N20240130-USSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSUSSSSSSSSSA000000000000000000000000000A000000000000000000U000000000000000000U000000000U000000000000000000",
        "ZZZZZZZ-ws0y1aet2cpq-Y-P20240130-USSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSUSSSSSSSSSA000000000000000000000000000A000000000000000000U000000000000000000U000000000U000000000000000000",
        "ZZZZZZZ-wo0y1met2cpq-Y-N20240130-USSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSUSSSSSSSSSA000000000000000000000000000A000000000000000000U000000000000000000U000000000U000000000000000000",
        "ZZZZZZZ-ws0y1met2czq-Y-N20240130-USSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSUSSSSSSSSSA000000000000000000000000000A000000000000000000U000000000000000000U000000000U000000000000000000",
        "ZZZZZZZ-ws0y1mft2cpq-Y-N20240130-USSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSUSSSSSSSSSA000000000000000000000000000A000000000000000000U000000000000000000U000000000U000000000000000000",
        "ZZZZZZZ-ws0y5met2cpq-Y-N20240130-USSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSUSSSSSSSSSA000000000000000000000000000A000000000000000000U000000000000000000U000000000U000000000000000000",
        "ZZZZZZZ-ws0y1met2cmq-Y-N20240130-USSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSUSSSSSSSSSUSSSSSSSSSA000000000000000000000000000A000000000000000000U000000000000000000U000000000U000000000000000000"
    ]
    zone_code = orginal_zone_code_from_tree_code(list)
    print(zone_code)