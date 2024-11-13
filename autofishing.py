import cv2
import numpy as np
import time
from pynput.mouse import Button, Controller
from pynput import keyboard  # pynput을 통해 키보드 리스너를 추가
import mss

class MinecraftAutoFishing:
    def __init__(self):
        self.mouse = Controller()
        self.sct = mss.mss()
        self.monitor = {
            'top': 400,
            'left': 700,
            'width': 500,
            'height': 300
        }
        self.running = True  # 프로그램 실행 상태
        self.paused = False   # 일시 정지 상태

    def capture_screen(self):
        screenshot = self.sct.grab(self.monitor)
        return np.array(screenshot)

    def detect_fishing_bob(self, frame):
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 110, 110])
        upper_red = np.array([10, 255, 255])
        mask = cv2.inRange(hsv, lower_red, upper_red)

        kernel = np.ones((5, 5), np.uint8)
        mask = cv2.erode(mask, kernel, iterations=2)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > 30]
            if valid_contours:
                largest_contour = max(valid_contours, key=cv2.contourArea)
                return cv2.boundingRect(largest_contour)
        return None

    def fish(self):
        print("자동 낚시를 시작합니다. 중단하려면 Ctrl+C를 누르세요.")
        self.right_click()
        time.sleep(2)

        last_positions = []  # 최근 위치를 저장할 리스트
        underwater_count = 0  # 물속 감지 횟수 카운터
        last_detection_time = time.time()  # 마지막 감지 시간

        while self.running:
            if not self.paused:  # 일시 정지 상태가 아닐 때만 실행
                frame = self.capture_screen()
                bob_rect = self.detect_fishing_bob(frame)

                if bob_rect:
                    x, y, w, h = bob_rect
                    print("낚시찌가 물에 떠 있습니다")

                    # 최근 위치를 업데이트
                    last_positions.append(y)
                    if len(last_positions) > 5:  # 최근 5개 위치만 유지
                        last_positions.pop(0)

                    # 마지막 감지 시간 업데이트
                    last_detection_time = time.time()

                    # 위치 변화 감지
                    if len(last_positions) >= 3:
                        avg_movement = np.mean(np.diff(last_positions[-3:]))  # 최근 3개의 위치 변화 평균
                        print(f"현재 Y 위치: {y}, 평균 변화: {avg_movement}")  # 디버깅 정보

                else:
                    # 낚시찌가 감지되지 않는 경우
                    if time.time() - last_detection_time > 0.5:  # 0.5초 이상 감지되지 않으면
                        print("낚시찌가 감지되지 않았습니다. 우클릭합니다.")
                        self.right_click()  # 낚시대 감기
                        time.sleep(1)
                        last_detection_time = time.time()  # 마지막 감지 시간 업데이트

                time.sleep(0.1)  # CPU 사용량 감소
            else:
                time.sleep(0.1)  # 일시 정지 상태일 때 CPU 사용량 감소

    def right_click(self):
        self.mouse.click(Button.right)

    def toggle_pause(self):  # 일시 정지 상태 토글 함수
        self.paused = not self.paused
        if self.paused:
            print("프로그램이 일시 정지되었습니다. TAB 키를 눌러 재개합니다.")
        else:
            print("프로그램이 재개되었습니다.")

def on_press(key, bot):
    try:
        if key == keyboard.Key.tab:  # TAB 키가 눌리면
            bot.toggle_pause()  # 일시 정지 상태 토글
    except AttributeError:
        pass

if __name__ == "__main__":
    print("5초 후 시작합니다. 마인크래프트 창을 활성화하세요.")
    time.sleep(5)
    
    bot = MinecraftAutoFishing()

    # 키보드 리스너 시작
    listener = keyboard.Listener(on_press=lambda key: on_press(key, bot))
    listener.start()

    bot.fish()
    listener.stop()  # 리스너 종료
    print("프로그램이 종료되었습니다.")

