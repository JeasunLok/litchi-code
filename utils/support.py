def group_by_time(data):
    grouped_data = {}
    for item in data:
        time = item[0]
        if time in grouped_data:
            grouped_data[time].append(item)
        else:
            grouped_data[time] = [item]
    return grouped_data

def encode_geohash(latitude, longitude, precision=12):
    """
    将纬度和经度编码为Geohash字符串。
    
    参数:
    latitude (float): 纬度
    longitude (float): 经度
    precision (int): Geohash字符串的长度，默认为12
    
    返回:
    str: Geohash编码的字符串
    """
    BASE32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    def encode_bits(value, range_min, range_max, bits):
        result = []
        for _ in range(bits):
            mid = (range_min + range_max) / 2
            if value > mid:
                result.append('1')
                range_min = mid
            else:
                result.append('0')
                range_max = mid
        return result

    lat_bits = encode_bits(latitude, -90, 90, precision * 5 // 2)
    lon_bits = encode_bits(longitude, -180, 180, precision * 5 // 2)

    bits = [None]*(len(lat_bits)+len(lon_bits))
    bits[::2] = lon_bits
    bits[1::2] = lat_bits

    hash_string = ''
    for i in range(0, len(bits), 5):
        n = int(''.join(bits[i:i+5]), 2)
        hash_string += BASE32[n]
    
    return hash_string

def initial_tree_phenology_code(lst, main_code, main_index):
    # grow_warning_code = "11"
    # disease_warning_code = "00"
    # phenology_code_length_list = [16, 16, 16, 4, 4, 12, 8, 8, 4, 8]
    
    # num_phenology = lst[3]
    # activate_index = main_index[num_phenology]
    # phenology_code_length = phenology_code_length_list[num_phenology]
    # phenology_code = main_code[activate_index:activate_index+phenology_code_length]
    # # print(phenology_code_length)
    # # print(num_phenology, lst)
    # # 白点期
    # if num_phenology == 4:
    #     # 白点率预警
    #     if lst[4] == 0:
    #         grow_warning_code = "00"
    #     elif lst[4] > 0:   
    #         grow_warning_code = "G0"
    #         disease_warning_code = "D0"

    #     # 新梢预警
    #     if lst[9] == 1:
    #         grow_warning_code = "G0"

    #     main_code = main_code[:activate_index+1] + grow_warning_code + disease_warning_code + main_code[activate_index+phenology_code_length+1:]    
        

    # elif num_phenology == 5:
        
    #     # # 在哪个表型
    #     # main_code = main_code[:activate_index+1] + grow_warning_code + disease_warning_code + main_code[activate_index+5:]  

    #     # 花蕾预警
    #     if lst[5] == 1:
    #         grow_warning_code = "G0"
    #         disease_warning_code = "D0"
        
    #         main_code = main_code[:activate_index+5] + grow_warning_code + disease_warning_code + main_code[activate_index+9:] 


    #     # 花苞预警
    #     if lst[6] == 1:
    #         grow_warning_code = "G0"
    #         disease_warning_code = "D0"

    #         main_code = main_code[:activate_index+9] + grow_warning_code + disease_warning_code + main_code[activate_index+13:] 


    #     # 花穗长度预警 等级待定
    #     if lst[3] > 10:
    #         grow_warning_code = "Ga"
  
    #         main_code = main_code[:activate_index+1] + grow_warning_code + disease_warning_code + main_code[activate_index+5:] 


    #     # 花量预警：爆花 等级待定
    #     if lst[4] > 0.7:
    #         grow_warning_code = "Gb"

    #         main_code = main_code[:activate_index+1] + grow_warning_code + disease_warning_code + main_code[activate_index+5:] 


    #     # 花带叶预警
    #     if lst[8] == 1 :
    #         if grow_warning_code == "11":
    #             grow_warning_code = "G0"

    #         main_code = main_code[:activate_index+1] + grow_warning_code + disease_warning_code + main_code[activate_index+5:] 



    # elif num_phenology == 6:
        
    #     # # 在哪个表型
    #     # main_code = main_code[:activate_index+1] + grow_warning_code + disease_warning_code + main_code[activate_index+5:]  

    #     # 谢花预警
    #     if lst[8] == 1 :
    #         grow_warning_code = "G0"

    #         main_code = main_code[:activate_index+5] + grow_warning_code + disease_warning_code + main_code[activate_index+9:] 

    #     # 开花预警
    #     if lst[10] == 1 :
    #         grow_warning_code = "G0"

    #         main_code = main_code[:activate_index+1] + grow_warning_code + disease_warning_code + main_code[activate_index+5:] 


    #     main_code = main_code[:activate_index] + grow_warning_code + disease_warning_code + main_code[activate_index+4:] 

    return main_code

def merge_tree_single_angle_code(lists):
    return 0

def merge_tree_two_angle_code(lists):
    sunny_code = lists[0]
    shady_code = lists[1]
    sunny_A = sunny_code.find("A")
    sunny_U = sunny_code.find("U", sunny_A)
    shady_A = shady_code.find("A")
    shady_U = shady_code.find("U", shady_A)
    last_code = shady_code[:shady_U] + sunny_code[sunny_A:]
    return last_code