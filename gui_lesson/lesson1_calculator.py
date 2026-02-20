"""
================================================================================
【1단계 실습: 간단한 계산기 GUI】
================================================================================
목표: 이전 카운터 예제를 확장해서 덧셈과 뺄셈이 가능한 계산기를 만들어봅니다.

배우는 것:
  1. 여러 개의 버튼 배치 (pack 메서드 복습)
  2. Entry 위젯: 사용자 입력 받기
  3. 버튼 클릭 시 입력값 가져오고 계산하기
  4. 여러 콜백 함수 관리

구조:
  ┌─────────────────────────┐
  │  숫자 입력창 (Entry)    │ ← 계산할 숫자 두 개 입력
  │  [+ 버튼] [- 버튼]     │ ← 연산 선택
  │  결과: 0               │ ← 계산 결과 표시
  └─────────────────────────┘
================================================================================
"""

import tkinter as tk


class CalculatorApp:
    a = 1
    """
    간단한 계산기 GUI 앱
    
    특징:
      - Entry 위젯으로 두 개의 숫자 입력받음
      - 덧셈/뺄셈 버튼으로 연산
      - 결과를 라벨에 표시
    """

    def __init__(self, root):
        """
        UI 초기화 함수
        
        매개변수:
            root (tk.Tk): 메인 윈도우 객체
        """
        
        # ─────────────────────────────────────────────────────────────────────
        # 【윈도우 설정】
        # ─────────────────────────────────────────────────────────────────────
        root.title("간단한 계산기")
        root.geometry("300x250")  # 🔑 윈도우 크기 지정: 너비 300px, 높이 250px
        
        # ─────────────────────────────────────────────────────────────────────
        # 【라벨 1: 제목】
        # ─────────────────────────────────────────────────────────────────────
        title_label = tk.Label(
            root,
            text="간단한 계산기",
            font=("Arial", 18, "bold")  # 🔑 굵은 글씨로 표시
        )
        title_label.pack(pady=10)
        
        # ─────────────────────────────────────────────────────────────────────
        # 【입력창 1: 첫 번째 숫자】
        # ─────────────────────────────────────────────────────────────────────
        label1 = tk.Label(root, text="첫 번째 숫자:", font=("Arial", 10))
        label1.pack()
        
        # 🔑 Entry: 사용자가 텍스트를 입력할 수 있는 위젯
        self.entry1 = tk.Entry(root, width=20)
        self.entry1.pack(padx=20, pady=5)
        
        # ─────────────────────────────────────────────────────────────────────
        # 【입력창 2: 두 번째 숫자】
        # ─────────────────────────────────────────────────────────────────────
        label2 = tk.Label(root, text="두 번째 숫자:", font=("Arial", 10))
        label2.pack()
        
        self.entry2 = tk.Entry(root, width=20)
        self.entry2.pack(padx=20, pady=5)
        
        # ─────────────────────────────────────────────────────────────────────
        # 【버튼 프레임】
        # 프레임: 여러 위젯을 그룹화할 때 사용 (레이아웃 관리 편함)
        # ─────────────────────────────────────────────────────────────────────
        button_frame = tk.Frame(root)
        button_frame.pack(pady=15)
        
        # 덧셈 버튼
        btn_add = tk.Button(
            button_frame,
            text="➕ 더하기",
            command=self.add,          # 🔑 덧셈 콜백 함수 연결
            width=12,
            bg="lightblue"             # 배경색 지정
        )
        btn_add.pack(side=tk.LEFT, padx=5)  # 🔑 side=tk.LEFT: 버튼을 왼쪽에 배치
        
        # 뺄셈 버튼
        btn_subtract = tk.Button(
            button_frame,
            text="➖ 빼기",
            command=self.subtract,     # 🔑 뺄셈 콜백 함수 연결
            width=12,
            bg="lightcoral"            # 배경색 지정
        )
        btn_subtract.pack(side=tk.LEFT, padx=5)

        btn_test_inset = tk.Button(
            button_frame,
            text ="insert_test",
            command=self.insert,
            width=12,
            bg="lightcoral" 
        )
        btn_test_inset.pack(side=tk.LEFT,padx=5)
        
        # ─────────────────────────────────────────────────────────────────────
        # 【결과 표시 라벨】
        # ─────────────────────────────────────────────────────────────────────
        self.result_label = tk.Label(
            root,
            text="결과: 0",
            font=("Arial", 14, "bold"),
            fg="green"                 # 글자색 지정
        )
        self.result_label.pack(pady=10)

    def insert(self):
        """
        insert 버튼 테스트:
        - 올바른 사용법: Entry.insert(index, text)
        - index: 정수(위치) 또는 tk.END(맨끝)
        이전 코드에서 발생한 TypeError 원인: insert에 문자열 인자를 주지 않아 발생합니다.
        """
        print("insert try")
        try:
            # 맨 끝에 '123' 문자열을 삽입하는 예시
            self.entry1.insert(tk.END, "insert_test")
        except TypeError as e:
            # 콘솔에 에러 원인 출력 (디버깅 용도)
            print("TypeError in insert:", e)


    def add(self):
        """
        덧셈 콜백 함수
        
        흐름:
            1. Entry 위젯에서 사용자 입력 가져오기 (.get() 메서드)
            2. 문자열을 정수로 변환
            3. 더하기
            4. 결과를 라벨에 업데이트
        """
        try:
            # 🔑 .get(): Entry에서 입력된 텍스트를 가져옴
            num1 = int(self.entry1.get())
            num2 = int(self.entry2.get())
            
            # 연산 수행
            result = num1 + num2

            self.entry1.delete(0, tk.END)  # 입력창 초기화
            self.entry2.delete(0, tk.END)

            
            # 🔑 .config(): 라벨의 텍스트 업데이트
            self.result_label.config(text=f"결과: {result}")
            # repaint(자바) => self.--.config(파이썬)
            
        except ValueError:
            # 🔑 사용자가 숫자가 아닌 값을 입력한 경우 처리
            self.result_label.config(text="❌ 숫자를 입력하세요!", fg="red")

    def subtract(self):
        """
        뺄셈 콜백 함수
        
        구조는 add() 함수와 동일하되, 연산만 다름
        """
        try:
            num1 = int(self.entry1.get())
            num2 = int(self.entry2.get())
            
            result = num1 - num2
            
            self.result_label.config(text=f"결과: {result}", fg="green")

            self.entry1.delete(0,tk.END)
            self.entry2.delete(0,tk.END)
            
        except ValueError:
            self.result_label.config(text="❌ 숫자를 입력하세요!", fg="red")


# ─────────────────────────────────────────────────────────────────────────────
# 【프로그램 시작】
# ─────────────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorApp(root)
    root.mainloop()


# ═════════════════════════════════════════════════════════════════════════════
# 【핵심 개념 정리】
# ═════════════════════════════════════════════════════════════════════════════
#
# 【1】Entry 위젯 (입력창)
#      용도: 사용자가 텍스트/숫자를 입력할 수 있는 필드
#      주요 메서드:
#        • .get()     → 입력된 텍스트를 문자열로 반환
#        • .delete()  → 입력된 텍스트 삭제
#        • .insert()  → 텍스트 삽입
#
# 【2】int() 함수
#      용도: 문자열을 정수로 변환
#      예제:
#        int("123")   → 123 (정수)
#        int("abc")   → ValueError (오류!)
#
# 【3】try-except 문
#      용도: 오류 발생 시 프로그램 중단 방지
#      구조:
#        try:
#            # 오류가 발생할 가능성이 있는 코드
#        except ValueError:
#            # ValueError 발생 시 실행할 코드
#
# 【4】Frame 위젯
#      용도: 여러 위젯을 그룹화 (레이아웃 관리 용이)
#      장점: 버튼들을 가로로 정렬할 때 유용
#
# 【5】pack() 의 side 매개변수
#      • pack()                    → 세로로 배치 (기본값)
#      • pack(side=tk.LEFT)        → 가로로 배치 (왼쪽부터)
#      • pack(side=tk.RIGHT)       → 가로로 배치 (오른쪽부터)
#
# 【6】위젯 속성 변경
#      • bg="색상"    → 배경색 변경
#      • fg="색상"    → 글자색 변경
#      • font=("Arial", 14, "bold") → 폰트/크기/스타일
#
 
#      사용자는 예상 밖의 입력을 할 수 있음 → 프로그램이 튕기는 것을 방지
#
# ═════════════════════════════════════════════════════════════════════════════