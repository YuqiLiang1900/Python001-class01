"""
自定义一个 python 函数，实现 map() 函数的功能。
"""


def my_map(func, *iterables):
    res_list = []
    if len(iterables) == 1:
        for item in iterables[0]:
            res = func(item)
            res_list.append(res)
    elif len(iterables) > 1:
        for pair_tuple in zip(*iterables):
            res = func(*pair_tuple)
            res_list.append(res)
    return iter(res_list)


if __name__ == '__main__':
    def my_func(n):
        return len(n)


    my_iterable = ('dragon fruit', 'strawberry', 'orange')
    original_map_res = map(my_func, my_iterable)
    print('The result of the original map function: ', list(original_map_res))
    my_map_res = my_map(my_func, my_iterable)
    print('The result of the self defined map function', list(my_map_res))


    def second_func(a, b):
        return a + b


    double_iterable = (('dragon fruit',), ('strawberry',))
    original_map_res = map(second_func, *double_iterable)
    print('The result of the original map function: ', list(original_map_res))
    my_map_res = my_map(second_func, *double_iterable)
    print('The result of the self defined map function', list(my_map_res))
