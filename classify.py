import cv2
import numpy as np
import pyautogui
import time

# 찾고자 하는 이미지 파일 경로
octopus_image_path = 'fish/문어.png'  # 문어 이미지 경로
sung_eo_image_path = 'fish/숭어.png'  # 숭어 이미지 경로

# 5초 대기
print("5초 후에 스크린샷을 찍습니다...")
time.sleep(5)

# 전체 화면 캡처
full_screenshot = pyautogui.screenshot()
full_screenshot_np = np.array(full_screenshot)

# BGR 포맷으로 변환
full_screenshot_bgr = cv2.cvtColor(full_screenshot_np, cv2.COLOR_RGB2BGR)

# 스크린샷 저장
screenshot_filename = 'full_screenshot.png'
cv2.imwrite(screenshot_filename, full_screenshot_bgr)
print(f"스크린샷이 '{screenshot_filename}'로 저장되었습니다.")

# 이미지 로드 및 회색조 변환
octopus_image = cv2.imread(octopus_image_path)
sung_eo_image = cv2.imread(sung_eo_image_path)

# ORB 특징 검출기 생성
orb = cv2.ORB_create()

# 특징점 및 기술자 계산
kp1, des1 = orb.detectAndCompute(octopus_image, None)
kp2, des2 = orb.detectAndCompute(sung_eo_image, None)

# BFMatcher 객체 생성
bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)

# 매칭 수행
matches_octopus = bf.match(des1, des2)
matches_sung_eo = bf.match(des2, des1)

# 매칭 결과 정렬
matches_octopus = sorted(matches_octopus, key=lambda x: x.distance)
matches_sung_eo = sorted(matches_sung_eo, key=lambda x: x.distance)

# 최소 거리 기준으로 필터링
good_matches_octopus = [m for m in matches_octopus if m.distance < 50]
good_matches_sung_eo = [m for m in matches_sung_eo if m.distance < 50]

# 결과 출력
if len(good_matches_octopus) > 0:
    print("Octopus found in the screenshot!")
else:
    print("No octopus found.")

if len(good_matches_sung_eo) > 0:
    print("Sung-eo found in the screenshot!")
else:
    print("No sung-eo found.")

# 윈도우 종료
cv2.destroyAllWindows()
