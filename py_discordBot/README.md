
## GUI/외부에서 연동하는 방법 (권장 2가지)
방법A — (권장) 파일을 약간 수정해 모듈식으로 사용
1. 수정 요지
  - `client.run(TOKEN)` 을 `if __name__ == "__main__": client.run(TOKEN)` 로 감싼다.
  - `start_bot(command: str | None = None)` 같은 함수를 추가해 `str_commend_line` 을 설정하고 봇을 실행하거나 비동기 루프를 제어하도록 만든다.

2. 장점
  - 같은 프로세스 내에서 GUI가 변수에 접근하거나 함수로 명령을 전달할 수 있어 통신이 쉬움.

3. 예시 패치(요약)
```python
# 상단에 전역 선언 유지
str_commend_line = ""

# 새 함수 추가 (파일 내)
def start_bot(command=None):
    global str_commend_line
    if command is not None:
        str_commend_line = command
    client.run(TOKEN)

# 파일 끝부분 수정
if __name__ == "__main__":
    client.run(TOKEN)
```

4. GUI에서 사용하는 예시 (동일 프로세스, 단일 스레드/스레드 사용 고려 필요)
```python
# gui_app.py
import threading
from py_discordBot import dsiocode_bot

def run_bot_with_command(cmd):
    # 봇을 별도 스레드로 실행
    t = threading.Thread(target=dsiocode_bot.start_bot, args=(cmd,), daemon=True)
    t.start()

# 버튼 이벤트 핸들러에서
run_bot_with_command("!add 12:00 점심시간 알림")
```

주의: discord.py 클라이언트는 비동기 이벤트 루프를 사용하므로 GUI와 같은 메인 스레드에서 직접 실행하면 충돌할 수 있습니다. 따라서 별도 프로세스나 스레드로 실행하고, 스레드/이벤트루프 간 통신을 안전하게 설계해야 합니다.
