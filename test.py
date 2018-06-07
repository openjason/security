def slope_of_price(my_list):
    #slope_v = 0
    slope = [sum(my_list[k: k + 4]) / float(len(my_list[k: k + 4])) for k in range(0, len(my_list), 4)]
    print (slope)
    print (slope[0]/slope[1])
    return slope



list=[16.36, 16.35, 16.37, 16.37, 16.37, 16.37, 16.37, 16.37, 16.37, 16.37]

slope_of_price(list)

