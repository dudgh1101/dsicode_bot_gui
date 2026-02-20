import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
from datetime import datetime
import threading

# ✅ 부모 디렉토리를 sys.path에 추가 (py_discordBot 모듈 찾기)
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from py_discordBot import discode_bot_test_git

# ✅ 명령어 딕셔너리 추가
commands = {
    "!add": "예약 추가 (시간 + 메시지)",
    "!remove": "예약 삭제 (시간)",
    "!remove all": "모든 예약 삭제",
    "!list": "예약 목록 보기",
    "!call_in": "음성 채널 입장",
    "!call_out": "음성 채널 퇴장",
    "!commend_list": "명령어 목록 보기",
    "!turn_off":"봇 종료"
}


class App:

    commend = ""

    def __init__(self, root):
        self.root = root
        self.bot_process = None          # 봇 프로세스 저장
        self.is_running = False          # 봇 실행 여부
        
        root.title("디스코드 gui앱")
        root.geometry("700x500")

        # ✅ 왼쪽 위에 상태만 표시
        self.status_label = tk.Label(root, text="OFF_AIR", font=("Arial", 15), fg="red",bg="white")
        self.status_label.place(x=10, y=10)

        # 현재 선택된 명령어 (중앙 정렬)
        self.commend_label = tk.Label(root, text="현재 선택된 명령어: 없음", font=("Arial", 12, "bold"), fg="blue")
        self.commend_label.pack(pady=10)

        # 입력 섹션 (중앙 정렬)
        input_frame = tk.Frame(root)
        input_frame.pack(pady=10)
        
        ttk.Label(input_frame, text="입력:").pack(side="left", padx=5)
        self.entry_input = tk.Entry(input_frame, width=35)
        self.entry_input.pack(side="left", padx=5)
        self.entry_input.insert(0, "12:00 알림")

        # 명령어 버튼 (중앙 정렬)
        label1 = tk.Label(root, text="📋 명령어 선택", font=("Arial", 10, "bold"))
        label1.pack(pady=10)

        frame = tk.Frame(root)
        frame.pack()

        for i, (cmd, label) in enumerate(commands.items()):
            if i % 2 == 0:  # 2개씩 새 줄
                btn_frame = tk.Frame(frame)
                btn_frame.pack()
            
            btn = tk.Button(btn_frame, text=cmd, command=lambda c=cmd: self.text_set(c), width=12)
            btn.pack(side=tk.LEFT, padx=5)
        
        run_btn = tk.Button(frame, text="실행", command=self.run, width=15)
        run_btn.pack(pady=10)

        # ✅ GUI 시작 시 자동으로 봇 시작
        self.start_bot()


    def text_set(self, commend):
        # commend 저장
        self.commend = commend
        
        # 시간이 필요한 명령어인지 확인
        if commend == "!add":
            # !add는 "12:00 메시지" 형식으로 입력받아서 파싱
            user_input = self.entry_input.get().strip()
            
            # 공백으로 구분하여 파싱 (첫 번째: 시간, 나머지: 메시지)
            parts = user_input.split(" ", 1)
            
            if len(parts) < 2:
                self.commend_label.config(text="❌ 형식: 12:00 메시지 (예: 12:00 점심)", fg="red")
                print("❌ 형식: 12:00 메시지")
                return
            
            time, msg = parts[0], parts[1]
            
            # 시간 형식 검증 (HH:MM)
            if len(time) != 5 or time[2] != ":":
                self.commend_label.config(text="❌ 시간 형식: HH:MM (예: 12:00)", fg="red")
                print("❌ 시간 형식 오류")
                return
            
            self.commend = f"!add {time} {msg}"
            self.commend_label.config(text=f"✅ 선택: {self.commend}", fg="green")
            print(f"선택됨: {self.commend}")
        
        elif commend == "!remove":
            # !remove는 시간만 입력받음
            user_input = self.entry_input.get().strip()
            
            if not user_input:
                self.commend_label.config(text="❌ 형식: 12:00 (예: 12:00)", fg="red")
                print("❌ 시간을 입력하세요")
                return
            
            # 시간 형식 검증
            if user_input.lower() == "all":
                self.commend = "!remove all"
            else:
                if len(user_input) != 5 or user_input[2] != ":":
                    self.commend_label.config(text="❌ 시간 형식: HH:MM 또는 all", fg="red")
                    print("❌ 시간 형식 오류")
                    return
                self.commend = f"!remove {user_input}"
            
            self.commend_label.config(text=f"✅ 선택: {self.commend}", fg="green")
            print(f"선택됨: {self.commend}")
        
        else:
            # 시간이 필요 없는 명령어
            self.commend_label.config(text=f"✅ 선택: {commend}", fg="green")
            print(f"선택됨: {commend}")

    def start_bot(self):
        # 봇을 별도 스레드에서 실행 (같은 프로세스)
        bot_thread = threading.Thread(
            target=discode_bot_test_git.start_bot,
            daemon=True
        )
        bot_thread.start()
        self.is_running = True  # ✅ 상태 업데이트
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🟢 봇이 시작되었습니다.")

    def stop_bot(self):
        """봇 프로세스 종료"""
        if not self.is_running or self.bot_process is None:
            print("❌ 실행 중인 봇이 없습니다.")
            return
        
        try:
            self.bot_process.terminate()
            self.is_running = False
            timestamp = datetime.now().strftime("%H:%M:%S")
            print(f"[{timestamp}] 🔴 봇이 종료되었습니다.")
        except Exception as e:
            print(f"❌ 봇 종료 실패: {str(e)}")

    def run(self):
        """
        Discord 봇에 명령어 전송
        str_commend_line 전역 변수에 저장하면 봇이 자동으로 읽음
        """
        if not self.commend:
            self.commend_label.config(text="❌ 명령어를 먼저 선택하세요!", fg="red")
            print("❌ 명령어를 먼저 선택하세요!")
            return
        
        # 봇이 실행 중인지 확인
        if not self.is_running:
            self.commend_label.config(text="❌ 봇을 먼저 시작하세요!", fg="red")
            print("❌ 봇을 먼저 시작하세요!")
            return
        
        # ✅ 전역 변수에 직접 저장 (봇이 읽음)
        if self.commend == "!call_in":
            self.status_label.config(text="ON_AIR",fg="green")
        elif self.commend == "!call_out":
            self.status_label.config(text="OFF_AIR",fg="red")
        discode_bot_test_git.str_commend_line = self.commend
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 📤 명령어 전송: {self.commend}")
        self.commend_label.config(text=f"📤 [{timestamp}] 전송됨: {self.commend}", fg="purple")
        



if __name__ == "__main__":

    root = tk.Tk()
    app = App(root)
    root.mainloop()