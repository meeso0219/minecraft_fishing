import tkinter as tk

class SimpleRegionViewer:
    def __init__(self):
        # 메인 창 생성
        self.root = tk.Tk()
        self.root.title("화면 영역 표시")
        
        # 창을 전체 화면으로 설정
        self.root.attributes('-fullscreen', True)
        
        # 항상 최상위에 표시
        self.root.attributes('-topmost', True)
        
        # 캡처 영역 설정
        self.capture_area = {
        'top': 100,
        'left': 100,
        'width': 500,
        'height': 300
        }

        
        # 캔버스 생성
        self.canvas = tk.Canvas(
            self.root,
            highlightthickness=0
        )
        self.canvas.pack(fill='both', expand=True)
        
        # ESC 키로 종료
        self.root.bind('<Escape>', lambda e: self.root.destroy())
        
        # 마우스 움직임 감지
        self.root.bind('<Motion>', self.on_mouse_move)
        
        # 좌표 표시 레이블
        self.coord_label = tk.Label(
            self.root,
            text="",
            bg='white',
            font=('Arial', 14)
        )
        self.coord_label.place(x=10, y=10)
        
        self.draw_region()
        
    def on_mouse_move(self, event):
        """마우스 좌표 업데이트"""
        self.coord_label.config(
            text=f'마우스 위치: X={event.x}, Y={event.y}\n'
                 f'캡처 영역: Top={self.capture_area["top"]}, '
                 f'Left={self.capture_area["left"]}\n'
                 f'Width={self.capture_area["width"]}, '
                 f'Height={self.capture_area["height"]}'
        )
    
    def draw_region(self):
        """캡처 영역 표시"""
        # 전체 화면을 연한 회색으로
        self.canvas.create_rectangle(
            0, 0,
            self.root.winfo_screenwidth(),
            self.root.winfo_screenheight(),
            fill='gray85'
        )
        
        # 캡처 영역을 노란색으로
        self.canvas.create_rectangle(
            self.capture_area['left'],
            self.capture_area['top'],
            self.capture_area['left'] + self.capture_area['width'],
            self.capture_area['top'] + self.capture_area['height'],
            fill='yellow',
            outline='red',
            width=2
        )
        
        # 안내 텍스트
        self.canvas.create_text(
            self.root.winfo_screenwidth() // 2,
            self.root.winfo_screenheight() - 50,
            text="ESC 키를 누르면 종료됩니다",
            font=('Arial', 14),
            fill='black'
        )

if __name__ == "__main__":
    print("화면 영역 표시 도구를 시작합니다...")
    print("노란색 사각형이 캡처 영역입니다.")
    print("ESC 키를 누르면 종료됩니다.")
    viewer = SimpleRegionViewer()
    viewer.root.mainloop()
