"""
作业一：
区分以下类型哪些是容器序列哪些是扁平序列，哪些是可变序列哪些是不可变序列：
list
tuple
str
dict
collections.deque
"""

# 容器序列：list, tuple, collections.deque
# 扁平序列：str
# 可变序列：list, collections.deque
# 不可变序列：str, tuple

"""
作业三：
实现一个 @timer 装饰器，记录函数的运行时间，注意需要考虑函数可能会接收不定长参数
"""
import time
from functools import wraps


def timer(func):
    @wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        end_time = time.time()
        run_time = end_time - start_time
        print('Finished {} in {} seconds.'.format(func.__name__, run_time))
        return res

    return wrapper_timer


@timer
def waste_some_time(num_times):
    for _ in range(num_times):
        sum([i ** 2 for i in range(10000)])


if __name__ == '__main__':
    waste_some_time(1)
