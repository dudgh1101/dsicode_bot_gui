# dsiocode_bot.py 설명서 (한글)

## 개요
- 위치: [py_discordBot/dsiocode_bot.py](py_discordBot/dsiocode_bot.py)
- 목적: 간단한 Discord 봇으로, DM(소유자 전용)을 통해 예약 메시지를 등록하고 지정된 채널에 정해진 시간에 전송합니다. 또한 서버에서 음성 채널 입장/퇴장 명령을 제공합니다.

## 필수 환경 변수 (.env 파일)
- `TOKEN` : Discord 봇 토큰
- `CHANNEL_ID` : 예약 메시지를 보낼 텍스트 채널 ID (정수)
- `OWNER_ID` : DM 명령을 사용할 수 있는 소유자(관리자) ID (정수)
- `VOICE_CHANNEL_ID` : 음성 채널 입장 명령에 사용할 음성 채널 ID (정수)

예시 .env:
TOKEN=your_token_here
CHANNEL_ID=123456789012345678
OWNER_ID=987654321098765432
VOICE_CHANNEL_ID=234567890123456789

## 주요 변수 및 역할
- `BASE_DIR`, `dotenv_path`, `load_dotenv(...)` : 현재 파일 위치에 있는 `.env` 로드
- `TOKEN`, `CHANNEL_ID`, `OWNER_ID`, `VOICE_CHANNEL_ID` : 위 환경 변수들
- `str_commend_line` : (현재 코드에서 초기화만 되어있음) GUI에서 보낼 명령어 문자열을 담는 용도로 의도됨. README 아래에서 활용/연동 방법 제안.
- `intents` : Discord 클라이언트 권한(메시지 내용, 멤버 등)
- `client` : `discord.Client` 인스턴스
- `user_scheduled_messages` : {user_id: {"HH:MM": [msg1, msg2, ...]}} 형태로 사용자별 예약 메시지 저장

## 핵심 함수/블록 설명
1) send_remaining_schedule_dm(user_id, channel)
- 특정 사용자(user_id)가 가진 예약 목록을 DM(또는 주어진 채널)으로 포맷해서 보냅니다.

2) class ShowScheduleButton(discord.ui.View)
- 디스코드 메시지에 붙일 수 있는 버튼을 구현합니다. 버튼 클릭 시 해당 사용자의 남은 예약 목록을 채널에 출력하고 버튼을 비활성화합니다.

3) async def send_scheduled_messages()
- 봇이 준비되면 백그라운드로 실행되는 루프입니다.
- 매 30초마다 현재 시각(Asia/Seoul, 형식 HH:MM)을 계산해 `user_scheduled_messages` 에 해당 시간이 있으면 메시지를 지정 채널에 전송합니다.
- 전송 시 `ShowScheduleButton` 뷰를 함께 붙입니다.

4) @client.event on_ready()
- 봇 로그인 후 호출됩니다. `send_scheduled_messages()` 작업을 루프에 태스크로 생성합니다.

5) @client.event on_message(message)
- 메시지 이벤트 핸들러입니다. 다음 기능을 처리합니다:
  - 서버 채널에서 `!call_in` / `!call_out` 명령: 음성 채널 입장/퇴장
  - DM에서 소유자(OWNER_ID)만 사용할 수 있는 명령들:
    - `!add HH:MM 메시지` : 예약 추가
    - `!remove HH:MM` 또는 `!remove all` : 예약 삭제
    - `!list` : 현재 예약 목록 보기
    - `!commend_list` : 사용 가능한 DM 명령 설명
    - `!turn_off` : 봇 종료

6) client.run(TOKEN)
- 파일을 실행하면 봇이 시작됩니다. 현재는 파일 최하단에 직접 실행 호출이 있어 import 하면 즉시 로그인하려고 시도합니다.

## 현재 코드에서 `str_commend_line` 의 상태
- 파일 상단에 `str_commend_line = ""` 로 초기화만 되어 있으며, 이후 코드에서 사용되지는 않습니다.
- 의도: 외부 GUI에서 버튼을 눌러 이 변수에 명령어를 넣고, 실행 시 그 내용을 참고해 동작시키려는 목적이라 추정됩니다.

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
