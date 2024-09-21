import pyautogui
import time
import threading
import keyboard

# 方法1：控制鼠标移动和点击
def move_and_click(stop_event):
    screen_width, screen_height = pyautogui.size()
    print(f"screen_width: {screen_width}, screen_height: {screen_height}")
    time.sleep(2)
    count = 1
    while not stop_event.is_set():  # 只要未收到停止信号，就持续运行
        # 移动鼠标到图片，并右击鼠标
        pyautogui.moveTo(684, 470, duration=0.2)
        time.sleep(0.2)
        pyautogui.rightClick()
        
        # 移动鼠标到图片另存为...，并左击鼠标
        pyautogui.moveTo(754, 521, duration=0.2)
        time.sleep(0.2)
        pyautogui.leftClick()

        # 移动鼠标到保存按钮，并左击鼠标
        pyautogui.moveTo(1123, 837, duration=0.2)
        time.sleep(0.2)
        pyautogui.leftClick()

        # 移动鼠标到下一张按钮，并左击鼠标
        pyautogui.moveTo(1089, 469, duration=0.2)
        time.sleep(0.5)
        pyautogui.leftClick()
        
        print(f'已成功保存{count}张图片！')
        count += 1
        
        

# 方法2：检测 'q' 键按下，按下时停止所有进程
def check_keyboard(stop_event):
    while True:
        if keyboard.is_pressed('q'):
            print("Detected 'q' key press. Stopping...")
            stop_event.set()  # 设置事件，用于通知停止
            break


# 方法3：实时获取鼠标位置
def get_mouse_position():
    try:
        while True:
            # 获取当前鼠标的位置
            x, y = pyautogui.position()
            # 打印鼠标的屏幕坐标
            print(f"Mouse position: X={x}, Y={y}   ", end='\r')  # 用 end='\r' 覆盖当前行
            time.sleep(0.1)  # 设置延迟，避免频繁打印
    except KeyboardInterrupt:
        print("\nStopped.")

if __name__ == '__main__':
    # 创建线程事件，用于在检测到 'q' 键按下时停止
    stop_event = threading.Event()

    # 创建两个线程，一个负责鼠标操作，另一个负责键盘检测
    mouse_thread = threading.Thread(target=move_and_click, args=(stop_event,))
    keyboard_thread = threading.Thread(target=check_keyboard, args=(stop_event,))

    # 启动线程
    mouse_thread.start()
    keyboard_thread.start()

    # 等待键盘检测线程结束
    keyboard_thread.join()

    # 停止鼠标线程
    mouse_thread.join()

    print("Threads have been stopped.")
    
    # get_mouse_position()
