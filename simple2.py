import tkinter as tk

class MonitorWindow:
    def __init__(self):
        # 주 모니터 설정
        self.monitor = {
            'top': 400,    # 화면 상단에서의 거리
            'left': 700,   # 화면 좌측에서의 거리
            'width': 500,  # 캡처할 영역의 너비
            'height': 300  # 캡처할 영역의 높이
        }
        
        # 메인 창 생성
        self.root = tk.Tk()
        self.root.title("캡처 영역 창")
        
        # 창 크기 설정
        self.root.geometry(f"{self.monitor['width']}x{self.monitor['height']}+{self.monitor['left']}+{self.monitor['top']}")
        
        # 창의 배경색 설정
        self.root.configure(bg='lightblue')
        
        # 종료 버튼
        close_button = tk.Button(self.root, text="종료", command=self.root.destroy)
        close_button.pack(pady=20)
        
        # 창 실행
        self.root.mainloop()

if __name__ == "__main__":
    app = MonitorWindow()
