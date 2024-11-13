import cv2
import numpy as np
import mss
import mss.tools
import tkinter as tk
from PIL import Image, ImageDraw

class RegionVisualizer:
    def __init__(self):
        self.root = tk.Tk()
        self.root.attributes('-alpha', 0.3)  # 창 투명도 설정
        self.root.attributes('-topmost', True)  # 항상 위에 표시
        self.root.overrideredirect(True)  # 창 테두리 제거
        
        # 모니터 정보 가져오기
        with mss.mss() as sct:
            monitor = sct.monitors[1]  # 기본 모니터
            self.screen_width = monitor["width"]
            self.screen_height = monitor["height"]
        
        # 캡처 영역 설정
        self.monitor = {
            'top': 400,
            'left': 700,
            'width': 500,
            'height': 300
        }
        
        # 캔버스 생성
        self.canvas = tk.Canvas(
            self.root,
            width=self.screen_width,
            height=self.screen_height,
            highlightthickness=0,
            bg='white'
        )
        self.canvas.pack()
        
        # ESC 키 바인딩
        self.root.bind('<Escape>', lambda e: self.root.quit())
        
        # 마우스 이벤트 바인딩
        self.canvas.bind('<Motion>', self.show_coordinates)
        
        # 좌표 표시 레이블
        self.coord_label = tk.Label(
            self.root,
            text="",
            bg='white',
            font=('Arial', 12)
        )
        self.coord_label.place(x=10, y=10)
        
    def show_coordinates(self, event):
        """마우스 좌표 표시"""
        x, y = event.x, event.y
        self.coord_label.config(
            text=f'마우스 위치 - X: {x}, Y: {y}\n'
                 f'캡처 영역 - Top: {self.monitor["top"]}, Left: {self.monitor["left"]}\n'
                 f'Width: {self.monitor["width"]}, Height: {self.monitor["height"]}'
        )
        
    def draw_region(self):
        """캡처 영역 표시"""
        # 반투명한 오버레이
        self.canvas.create_rectangle(
            0, 0,
            self.screen_width, self.screen_height,
            fill='gray85'
        )
        
        # 캡처 영역 강조
        self.canvas.create_rectangle(
            self.monitor['left'],
            self.monitor['top'],
            self.monitor['left'] + self.monitor['width'],
            self.monitor['top'] + self.monitor['height'],
            fill='yellow',
            outline='red',
            width=2
        )
        
        # 설명 텍스트
        self.canvas.create_text(
            self.screen_width // 2,
            self.screen_height - 50,
            text="ESC 키를 누르면 종료됩니다.",
            font=('Arial', 14),
            fill='black'
        )
        
    def run(self):
        """시각화 도구 실행"""
        self.draw_region()
        print("캡처 영역을 표시합니다. ESC 키를 누르면 종료됩니다.")
        self.root.mainloop()

if __name__ == "__main__":
    visualizer = RegionVisualizer()
    visualizer.run()