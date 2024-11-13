import pyautogui
import time
from pynput import keyboard  # pynput is better on MacOS

# 종료 상태를 저장할 변수
running = True
paused = False  # 일시 정지 상태를 저장할 변수

def on_press(key):
    global running, paused
    try:
        if key == keyboard.Key.tab:  # TAB 키가 눌리면
            paused = not paused  # 일시 정지 상태 토글
            if paused:
                print("프로그램이 일시 정지되었습니다. TAB 키를 눌러 재개합니다.")
            else:
                print("프로그램이 재개되었습니다.")
    except AttributeError:
        pass

def main():
    global running, paused
    time.sleep(5)
    print("프로그램이 시작되었습니다. TAB 키를 눌러 일시 정지하거나 재개합니다.")
    
    # 키보드 리스너 시작
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while running:
            if not paused:  # 일시 정지 상태가 아닐 때만 클릭
                # 마우스 좌클릭
                pyautogui.click()
                time.sleep(0.15)  # 클릭 간격 조정

    finally:
        listener.stop()  # 리스너 종료
        print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()
