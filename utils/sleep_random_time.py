import time
import random

def sleep_random_time(min_seconds, max_seconds):
    """
    让程序在给定的时间区间内随机生成时间数进行睡眠。
    
    :param min_seconds: 最小睡眠时间（秒）
    :param max_seconds: 最大睡眠时间（秒）
    """
    # 生成一个在 min_seconds 和 max_seconds 之间的随机时间
    sleep_time = random.uniform(min_seconds, max_seconds)
    
    # 打印生成的睡眠时间（可选）
    # print(f"Sleeping for {sleep_time:.2f} seconds")
    
    # 让程序暂停指定的时间
    time.sleep(sleep_time)

if __name__ == '__main__':
	sleep_random_time(1, 5)  # 在 1 到 5 秒之间随机生成睡眠时间
