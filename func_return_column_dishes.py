def column_dishes(item_category):
    if item_category == 'salads':
        column_num = 3
        column_price = 4

    elif item_category == 'sup':
        column_num = 5
        column_price = 6

    elif item_category == 'noodles':
        column_num = 7
        column_price = 8

    elif item_category == 'garnish':
        column_num = 9
        column_price = 10

    elif item_category == 'burger':
        column_num = 11
        column_price = 12
    elif item_category == 'sweets':
        column_num = 13
        column_price = 14

    return [column_num, column_price]