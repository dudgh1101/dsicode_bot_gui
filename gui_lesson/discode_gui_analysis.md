# discode_gui.py 코드 분석

## 1. 개요

`discode_gui.py`는 **Tkinter** 기반의 GUI 애플리케이션으로, **Discord 봇**을 GUI에서 제어할 수 있게 하는 프로그램입니다. 사용자가 GUI 버튼을 클릭하면 해당 명령어가 Discord 봇으로 전송되어 예약을 추가하거나 음성 채널을 제어할 수 있습니다.

---

## 2. 전체 구조도

```
┌─────────────────────────────────────────────────────────────────┐
│                        GUI Application                          │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────────────────┐ │
│  │ 상태 표시   │  │ 명령어 선택  │  │ 입력 필드                │ │
│  │ (ON_AIR/   │  │ 버튼 그리드  │  │ (시간+메시지 입력)       │ │
│  │  OFF_AIR)  │  │ (!add, etc) │  │                         │ │
│  └─────────────┘  └─────────────┘  └─────────────────────────┘ │
│                            │                                    │
│                            ▼                                    │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │            Thread: Discord Bot (same process)              ││
│  │  ┌──────────────────┐  ┌──────────────────────────────────┐││
│  │  │ str_commend_line │◄─┼── 전역 변수로 명령어 수신         │││
│  │  │ (공유 변수)      │  │  check_gui_command() 비동기 루프 │││
│  │  └──────────────────┘  └──────────────────────────────────┘││
│  └─────────────────────────────────────────────────────────────┘│
└─────────────────────────────────────────────────────────────────┘
```

---

## 3. 주요 기능

| 명령어 | 기능 | 필요 입력 |
|--------|------|-----------|
| `!add` | 예약 추가 (시간 + 메시지) | `12:00 점심알림` |
| `!remove` | 예약 삭제 | `12:00` or `all` |
| `!remove all` | 모든 예약 삭제 | 없음 |
| `!list` | 예약 목록 보기 | 없음 |
| `!call_in` | 음성 채널 입장 | 없음 |
| `!call_out` | 음성 채널 퇴장 | 없음 |
| `!commend_list` | 명령어 목록 보기 | 없음 |
| `!turn_off` | 봇 종료 | 없음 |

---

## 4. 코드 분석

### 4.1 임포트 및 초기화

```python
import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os
from datetime import datetime
import threading
```

| 모듈 | 용도 |
|------|------|
| `tkinter` / `ttk` | GUI 구성 요소 |
| `threading` | Discord 봇을 별도 스레드에서 실행 |
| `datetime` | 로그 타임스탬프용 |
| `os` / `sys` | 경로 처리 및 모듈 import |

### 4.2 모듈 경로 설정

```python
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from py_discordBot import discode_bot_test_git
```

**원리**: 현재 파일의 부모 디렉토리를 `sys.path`에 추가하여 상위 디렉토리에 있는 `py_discordBot` 모듈을 import할 수 있게 합니다. 이는 패키지 구조가 아닌 상태에서 모듈을 참조하기 위한 패턴입니다.

### 4.3 명령어 딕셔너리

```python
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
```

GUI 버튼 생성 시 이 딕셔너리를 순회하며 버튼을 동적으로 생성합니다.

---

## 5. App 클래스 상세 분석

### 5.1 생성자 `__init__`

```python
def __init__(self, root):
    self.root = root
    self.bot_process = None
    self.is_running = False
    
    root.title("디스코드 gui앱")
    root.geometry("700x500")
```

**역할**:
- Tkinter 루트 윈도우 초기화
- 윈도우 크기 및 제목 설정

### 5.2 UI 구성 요소

#### 상태 표시 라벨
```python
self.status_label = tk.Label(root, text="OFF_AIR", font=("Arial", 15), fg="red",bg="white")
self.status_label.place(x=10, y=10)
```
- `place()` 레이아웃 관리자 사용
- `OFF_AIR`(빨강) / `ON_AIR`(초록) 두 상태 표시
- 음성 채널 입퇴장 명령 시 상태 변경

#### 현재 선택된 명령어 표시
```python
self.commend_label = tk.Label(root, text="현재 선택된 명령어: 없음", font=("Arial", 12, "bold"), fg="blue")
self.commend_label.pack(pady=10)
```
- `pack()`으로 중앙 정렬
- 사용자가 버튼 클릭 시 선택된 명령어 표시

#### 입력 필드
```python
input_frame = tk.Frame(root)
ttk.Label(input_frame, text="입력:").pack(side="left", padx=5)
self.entry_input = tk.Entry(input_frame, width=35)
self.entry_input.pack(side="left", padx=5)
self.entry_input.insert(0, "12:00 알림")
```

### 5.3 명령어 버튼 생성

```python
for i, (cmd, label) in enumerate(commands.items()):
    if i % 2 == 0:
        btn_frame = tk.Frame(frame)
        btn_frame.pack()
    
    btn = tk.Button(btn_frame, text=cmd, command=lambda c=cmd: self.text_set(c), width=12)
    btn.pack(side=tk.LEFT, padx=5)
```

**핵심 포인트 - 클로저 문제 해결**:
```python
lambda c=cmd: self.text_set(c)
```
Python의 루프에서 람다를 사용할 때 발생하는 **클로저 문제**를 해결하기 위해 기본 인자 `c=cmd`를 사용합니다. 이 패턴이 없으면 모든 버튼이 마지막 명령어만 참조하게 됩니다.

### 5.4 자동 시작 및 종료 처리

```python
self.start_bot()  # GUI 시작 시 봇 자동 실행
root.protocol("WM_DELETE_WINDOW", self.on_closing)  # X 버튼 처리
```

---

## 6. 메서드 분석

### 6.1 `text_set(commend)` - 명령어 처리

```python
def text_set(self, commend):
    self.commend = commend
    
    if commend == "!add":
        # 파싱: "12:00 메시지" → 시간, 메시지 분리
        parts = user_input.split(" ", 1)
        time, msg = parts[0], parts[1]
        
        # 시간 형식 검증: HH:MM
        if len(time) != 5 or time[2] != ":":
            # 오류 처리
            return
        
        self.command = f"!add {time} {msg}"
```

**시간 검증 로직**:
- 길이가 5자리가 아닌 경우: `123:00` (4자리), `12:000` (5자리 but 마지막이 숫자)
- 3번째 문자가 `:`가 아닌 경우: `12-00`, `12.00`

### 6.2 `start_bot()` - 봇 실행

```python
def start_bot(self):
    bot_thread = threading.Thread(
        target=discode_bot_test_git.start_bot,
        daemon=True
    )
    bot_thread.start()
    self.is_running = True
```

**핵심 원리**:
1. **별도 스레드에서 실행**: GUI 메인 루프를 블로킹하지 않음
2. **daemon=True**: GUI 종료 시 스레드도 함께 종료
3. **동일 프로세스**: `py_discordBot` 모듈의 `str_commend_line` 전역 변수를 공유

### 6.3 `run()` - 명령어 전송

```python
def run(self):
    if not self.command:
        # 오류: 명령어 미선택
        return
    
    if not self.is_running:
        # 오류: 봇 미실행
        return
    
    # 음성 채널 상태 업데이트
    if self.command == "!call_in":
        self.status_label.config(text="ON_AIR", fg="green")
    elif self.command == "!call_out":
        self.status_label.config(text="OFF_AIR", fg="red")
    
    # 전역 변수에 명령어 저장 → 봇이 읽음
    discode_bot_test_git.str_commend_line = self.command
```

**GUI ↔ Bot 통신 원리**:

```
GUI (run())              Discord Bot (check_gui_command())
    │                            │
    │ str_commend_line = cmd    │
    │ ───────────────────────►  │
    │                            │ while loop에서 1초마다 확인
    │                    읽음 → 처리 → 초기화
```

### 6.4 `on_closing()` - 종료 처리

```python
def on_closing(self):
    print("GUI를 закрытие합니다. 봇도 종료...")
    
    # 종료 명령어 전송
    discode_bot_test_git.str_commend_line = "!turn_off"
    
    # 0.5초 후 GUI 종료
    self.root.after(500, self.root.destroy)
```

---

## 7. Discord Bot 연동 분석

### 7.1 통신 방식

| 방식 | 설명 |
|------|------|
| **전역 변수 공유** | `str_commend_line` 문자열을 통해 명령어 전달 |
| **동일 프로세스** | 스레드로同一个 프로세스에서 실행 |
| **폴링 방식** | 봇이 1초마다 전역 변수 확인 |

### 7.2 discode_bot_test_git 모듈 구조

```
┌────────────────────────────────────────────────────────────┐
│               discode_bot_test_git.py                     │
├────────────────────────────────────────────────────────────┤
│  str_commend_line = ""     # 전역 명령어 변수             │
│                                                            │
│  ┌──────────────────┐  ┌─────────────────────────────┐    │
│  │ check_gui_       │  │ send_scheduled_messages()  │    │
│  │ command()       │  │ - 30초마다 예약 메시지 전송 │    │
│  │ - 1초마다 확인   │  │ - 시간되면 Discord로 전송  │    │
│  │ - GUI 명령어 처리│  └─────────────────────────────┘    │
│  └──────────────────┘                                      │
│                                                            │
│  ┌──────────────────┐  ┌─────────────────────────────┐    │
│  │ user_scheduled   │  │ ShowScheduleButton          │    │
│  │ _messages {}    │  │ - Discord UI 버튼           │    │
│  │ - 예약 저장소    │  │ - 남은 일정 보기            │    │
│  └──────────────────┘  └─────────────────────────────┘    │
└────────────────────────────────────────────────────────────┘
```

---

## 8. 설계 패턴 및 원리

### 8.1 MVC 패턴

| 구성요소 | 해당 코드 |
|----------|----------|
| **Model** | `user_scheduled_messages` 딕셔너리, `str_commend_line` |
| **View** | Tkinter UI (라벨, 버튼, 입력 필드) |
| **Controller** | `App` 클래스의 메서드들 (`text_set`, `run`, `on_closing`) |

### 8.2 스레딩 패턴

```python
# 메인 스레드: GUI 이벤트 루프
root.mainloop()

# 워커 스레드: Discord 봇 (non-blocking)
threading.Thread(target=start_bot, daemon=True)
```

### 8.3 폴링(Polling) 패턴

```python
# Discord Bot側
while not client.is_closed():
    if str_commend_line:  # 전역 변수 확인
        # 명령어 처리
        str_commend_line = ""  # 초기화
    await asyncio.sleep(1)
```

---

## 9. 데이터 흐름

### 명령어 전송流程

```
1. 사용자가 버튼 클릭
       │
       ▼
2. text_set(cmd) 호출
   - !add: 입력값 파싱 (시간+메시지)
   - 시간 형식 검증
   - 명령어 문자열组装
       │
       ▼
3. "실행" 버튼 클릭 → run() 호출
   - 상태Label 업데이트 (call_in/out 시)
   - str_commend_line = 명령어
       │
       ▼
4. Discord Bot (별도 스레드)
   - 1초마다 폴링
   - 명령어 감지 → 처리
   - DM으로 결과 전송
       │
       ▼
5. str_commend_line = "" (초기화)
```

---

## 10. 주요 고려사항

### 10.1 장점
- **간단한 통신**: 전역 변수로 간단하게 명령어 전달
- **동일 프로세스**: 모듈 import로 직접 함수 호출 가능
- **비동기 처리**: Discord 봇은 async, GUI는 별도 스레드로 분리

### 10.2 개선 가능 사항
- **스레드 안전성**: `str_commend_line` 접근 시 Lock 필요
- **에러 처리**: 네트워크 단절 시 재연결 로직 부재
- **UI 반응성**: 장시간 작업 시 별도 스레드 필요
- **설정 외부화**: TOKEN, CHANNEL_ID 등이 하드코딩

---

## 11. 실행 흐름 요약

```
┌─────────────────┐
│  python 실행    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  App.__init__  │
│  - UI 생성      │
│  - start_bot() │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌───────────────┐
│ GUI   │  │ Discord Bot  │
│ 스레드│  │ (async 루프) │
└───┬───┘  └───────┬───────┘
    │              │
    │  str_commend_line
    │◄─────────────┘
    │              │
    │  버튼 클릭   │
    │─────────────►│
    │              │
    │  명령어 처리 │
    │              │
```

---

## 12. 결론

`discode_gui.py`는 **Tkinter GUI**와 **Discord Bot**을 **同一 프로세스 내 별도 스레드**로 실행하고, **전역 변수 폴링**을 통해 명령어를 전달하는 간단하지만 효과적인アーキ텍처를 채택하고 있습니다.

핵심 원리는:
1. **GUI**는 사용자 입력을 받아 명령어를 조합
2. **전역 변수** `str_command_line`에 명령어 저장
3. **Discord Bot**의 비동기 루프가 1초마다 폴링하여 명령어 처리
4. 결과를 **DM**으로 사용자에게 전송

이 구조는 간단하지만, 실제 프로덕션에서는 **threading.Lock**이나 **queue**를 사용한 더 안전한 통신 방식을 고려할 수 있습니다.
