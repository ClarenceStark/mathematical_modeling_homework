def get_possible_numbers(self_number, ang1): #接受自身编号self_number 和 未知编号的飞机发射的信号所得到的信息角ang1 为参数，确定发射信号的未知编号飞机的2个可能编号
    return(round(self_number + (180 - 2 * ang1) / 40), round(self_number - (180 - 2 * ang1) / 40))

def get_certain_number(self_number, ang1, actual_ang2): #接受发射信号的未知编号飞机向FY01飞机发射信号所得到的信息角actual_ang2为参数，确定其实际编号
    possible_numbers = get_possible_numbers(self_number, ang1)
    expected_ang2_01 = abs(180 - (possible_numbers[0] - 1) * 40) / 2
    expected_ang2_02 = abs(180 - (possible_numbers[1] - 1) * 40) / 2
    return possible_numbers[0] if abs(expected_ang2_01 - actual_ang2) < abs(expected_ang2_02 - actual_ang2) else possible_numbers[1]
        
print(get_certain_number(4, 50, 60))