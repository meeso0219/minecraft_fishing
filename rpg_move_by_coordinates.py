import pytesseract
from PIL import ImageGrab, ImageEnhance, ImageOps, ImageFilter, Image
import time
import os
import pyautogui
from pynput import keyboard
import random
import threading

# Tesseract 설치 경로 설정
pytesseract.pytesseract.tesseract_cmd = r'/opt/homebrew/bin/tesseract'

# 캡처할 화면 영역의 좌표 설정
x1, y1, x2, y2 = 45, 230, 350, 255

# 캡처 폴더 경로 설정
capture_folder = "captures"

# 'captures' 폴더가 없는 경우 생성
if not os.path.exists(capture_folder):
    os.makedirs(capture_folder)

# 전역 변수 설정
running = False
paused = True
movement_thread = None

def preprocess_image(image):
    image = ImageOps.grayscale(image)
    threshold = 128
    image = image.point(lambda p: p > threshold and 255)
    image = image.resize((image.width * 2, image.height * 2), Image.LANCZOS)
    image = image.filter(ImageFilter.GaussianBlur(radius=1))
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(1.5)
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)
    return image

def capture_and_read_coordinates():
    screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
    processed_image = preprocess_image(screenshot)
    custom_config = r'--oem 3 --psm 11 -c tessedit_char_whitelist=0123456789.-XYZ:/'
    text = pytesseract.image_to_string(processed_image, config=custom_config)

    print("OCR 인식 결과:")
    print(text)

    if text.strip():
        return parse_coordinates(text)
    return None, None

def parse_coordinates(text):
    try:
        coordinates = text.split('/')
        x = int(float(coordinates[0].strip()))
        z = int(float(coordinates[2].split(':')[0].strip()))
        return x, z
    except (IndexError, ValueError) as e:
        print(f"좌표를 파싱하는 데 오류가 발생했습니다: {e}")
        return None, None

def adjust_position():
    key = random.choice(['w', 'a', 's', 'd'])
    pyautogui.keyDown(key)
    time.sleep(0.1)
    pyautogui.keyUp(key)

def move_to_target(target_x, target_z):
    global running, paused
    while running:
        if not running:  # 완전 종료 체크
            break
            
        if paused:  # 일시정지 체크
            time.sleep(0.1)
            continue

        current_x, current_z = capture_and_read_coordinates()
        if current_x is None or current_z is None:
            adjust_position()
            continue

        x_diff = target_x - current_x
        z_diff = target_z - current_z
        
        if abs(x_diff) > 1 or abs(z_diff) > 1:
            if abs(x_diff) > abs(z_diff):
                if x_diff > 0:
                    pyautogui.keyDown('w')
                    time.sleep(1)
                    pyautogui.keyUp('w')
                else:
                    pyautogui.keyDown('s')
                    time.sleep(1)
                    pyautogui.keyUp('s')
            else:
                if z_diff > 0:
                    pyautogui.keyDown('d')
                    time.sleep(1)
                    pyautogui.keyUp('d')
                else:
                    pyautogui.keyDown('a')
                    time.sleep(1)
                    pyautogui.keyUp('a')
        else:
            print(f"목표 좌표 근처입니다. 현재 좌표: X:{current_x}, Z:{current_z}")
            
        time.sleep(0.5)

def start_movement(target_x, target_z):
    global movement_thread
    movement_thread = threading.Thread(target=move_to_target, args=(target_x, target_z))
    movement_thread.daemon = True  # 메인 스레드가 종료되면 같이 종료되도록 설정
    movement_thread.start()

def on_press(key):
    global running, paused
    try:
        if key == keyboard.KeyCode.from_char('='):
            print("프로그램을 종료합니다.")
            running = False
            return False  # 리스너 중지

        if key == keyboard.Key.tab:
            if not running:
                running = True
                paused = False
                print("프로그램이 시작되었습니다.")
                start_movement(target_x, target_z)
            else:
                paused = not paused
                print("프로그램이 일시정지되었습니다." if paused else "프로그램이 재개되었습니다.")
    except AttributeError:
        pass

def main():
    global target_x, target_z, running, paused
    target_x = -20
    target_z = -70
    running = False
    paused = True

    print("프로그램 조작 방법:")
    print("- 탭(Tab) 키: 프로그램 시작/일시정지 토글")
    print("- '=' 키: 프로그램 완전 종료")

    with keyboard.Listener(on_press=on_press) as listener:
        try:
            listener.join()
        except KeyboardInterrupt:
            print("\n프로그램이 강제 종료되었습니다.")
        finally:
            running = False
            print("프로그램이 종료되었습니다.")

if __name__ == "__main__":
    main()