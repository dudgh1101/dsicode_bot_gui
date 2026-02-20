from dotenv import load_dotenv
import os
import runpy    
import threading
import py_discordBot.discode_bot as dsiocode_bot

# .env 파일의 전체 경로 지정
load_dotenv()

# 환경 변수 읽기
print(os.getenv("TOKEN"))
print(os.getenv("OWNER_ID"))
print(os.getenv("VOICE_CHANNEL_ID"))
print(os.getenv("CHANNEL_ID"))

print("전부 출력 완료")

def run_bot_with_command(cmd):
    # 봇을 별도 스레드로 실행
    t = threading.Thread(target=dsiocode_bot.start_bot, args=(cmd,), daemon=True)
    t.start()

# runpy.run_path("/Users/user/Desktop/python/py_discordBot/dsiocode_bot.py")