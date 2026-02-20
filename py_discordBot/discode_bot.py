import discord
import asyncio
from datetime import datetime
import pytz
from dotenv import load_dotenv
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path)

print(os.getenv("Token"))
# pip install wheel
# pip install PyNaCl
#필수 설치 라이브러리
# ────────── 설정 ──────────
TOKEN = os.getenv("TOKEN")
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))
OWNER_ID = int(os.getenv("OWNER_ID"))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID"))
# ──────────────────────────

str_commend_line = ""

intents = discord.Intents.default()
intents.messages = True 
intents.guilds = True
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)

# 사용자별 예약 메시지 저장
user_scheduled_messages = {}

# ────────── DM에서 남은 일정 표시 ──────────
async def send_remaining_schedule_dm(user_id, channel):
    if user_id in user_scheduled_messages and user_scheduled_messages[user_id]:
        sorted_times = sorted(user_scheduled_messages[user_id].keys())
        msg_list = "\n".join(
            [f"⏰ {time}: {', '.join(user_scheduled_messages[user_id][time])}" for time in sorted_times]
        )
        await channel.send(f"📅 현재 예약된 메시지 목록:\n{msg_list}")
    else:
        await channel.send("📭 현재 예약된 메시지가 없습니다.")

# ────────── 버튼 클래스 ──────────
class ShowScheduleButton(discord.ui.View):
    def __init__(self, user_id):
        super().__init__(timeout=None)
        self.user_id = user_id

    @discord.ui.button(label="남은 일정 보기", style=discord.ButtonStyle.green)
    async def show_schedule(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        if self.user_id in user_scheduled_messages and user_scheduled_messages[self.user_id]:
            sorted_times = sorted(user_scheduled_messages[self.user_id].keys())
            msg_list = "\n".join(
                [f"⏰ {time}: {', '.join(user_scheduled_messages[self.user_id][time])}" for time in sorted_times]
            )
            await interaction.channel.send(f"📅 앞으로 남은 예약 메시지 목록:\n{msg_list}")
        else:
            await interaction.channel.send("📭 앞으로 남은 예약 메시지가 없습니다.")
        button.disabled = True
        await interaction.message.edit(view=self)

# ────────── 예약 메시지 전송 ──────────
async def send_scheduled_messages():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    if channel is None:
        print("❌ 채널을 찾을 수 없습니다.")
        return

    timezone = pytz.timezone("Asia/Seoul")
    while not client.is_closed():
        now = datetime.now(timezone).strftime("%H:%M")
        for user_id, schedule in user_scheduled_messages.items():
            if now in schedule:
                messages = schedule[now]
                for msg in messages:
                    try:
                        view = ShowScheduleButton(user_id)
                        await channel.send(f"📢 {msg}", view=view)
                    except Exception as e:
                        print(f"⚠️ 메시지 전송 오류: {e}")
                del schedule[now]
        await asyncio.sleep(30)

# ────────── 이벤트 ──────────
@client.event
async def on_ready():
    print(f"✅ Logged in as {client.user}")
    print("작업을 처리할 준비가 되었어요.")
    client.loop.create_task(send_scheduled_messages())

def start_bot(command=None):
    global str_commend_line
    if command is not None:
        str_commend_line = command
    client.run(TOKEN)


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # ────────── 서버 명령어: call_in / call_out ──────────
    if message.content.startswith("!call_in") or message.content.startswith("!call_out"):
        if message.guild is None:
            await message.channel.send("❌ 이 명령어는 서버 내에서만 사용할 수 있습니다.")
            return

        # call_in
        if message.content.startswith("!call_in"):
            channel = client.get_channel(VOICE_CHANNEL_ID)
            if channel and isinstance(channel, discord.VoiceChannel):
                if message.guild.voice_client is None:
                    await channel.connect()
                    await message.channel.send(f"🎤 봇이 지정된 통화방 **{channel.name}** 에 입장했습니다!")
                else:
                    await message.channel.send("⚠️ 이미 통화방에 연결되어 있습니다.")
            else:
                await message.channel.send("❌ VOICE_CHANNEL_ID가 올바르지 않습니다.")

        # call_out
        elif message.content.startswith("!call_out"):
            voice_client = message.guild.voice_client
            if voice_client:
                await voice_client.disconnect()
                await message.channel.send("👋 봇이 통화방에서 퇴장했습니다.")
            else:
                await message.channel.send("❌ 봇이 통화방에 연결되어 있지 않습니다.")
        return  # 서버 명령어 처리 후 종료

    # ────────── DM 명령어 처리 ──────────
    if not isinstance(message.channel, discord.DMChannel):
        return

    user_id = message.author.id
    if user_id != OWNER_ID:
        await message.author.send("⚠️ 권한이 없습니다.")
        return

    try:
        # 메시지 추가
        if message.content.startswith("!add"):
            parts = message.content.split(" ", 2)
            if len(parts) < 3:
                await message.author.send("❌ 올바른 형식: `!add HH:MM 메시지`")
                return
            _, time, msg = parts
            if len(time) != 5 or time[2] != ":":
                await message.author.send("❌ 시간은 HH:MM 형식으로 입력해주세요!")
                return
            user_scheduled_messages.setdefault(user_id, {}).setdefault(time, []).append(msg)
            await message.author.send(f"✅ {time}에 메시지가 추가되었습니다: \"{msg}\"")

        # 삭제
        elif message.content.startswith("!remove"):
            parts = message.content.split(" ", 1)
            if len(parts) < 2:
                await message.author.send("❌ 올바른 형식: `!remove HH:MM`")
                return
            _, time = parts
            if time.lower() == "all":
                user_scheduled_messages[user_id] = {}
                await message.author.send("🗑 모든 예약 메시지가 삭제되었습니다.")
            elif user_id in user_scheduled_messages and time in user_scheduled_messages[user_id]:
                del user_scheduled_messages[user_id][time]
                await message.author.send(f"🗑 {time} 예약 메시지를 삭제했습니다.")
            else:
                await message.author.send(f"⚠️ {time}에 설정된 메시지가 없습니다.")

        # 전체 일정 보기
        elif message.content.startswith("!list"):
            await send_remaining_schedule_dm(user_id, message.author)

        elif message.content.startswith("!commend_list"):
            await message.author.send(
                ":eight_spoked_asterisk: !list: 지금까지 설정된 모든 일정을 표시합니다.\n"
                ":eight_spoked_asterisk: !add: !add HH:MM 메시지 형태로 입력하여 일정을 추가할 수 있습니다.\n"
                ":eight_spoked_asterisk: !remove: !remove HH:MM 형식으로 해당 시간의 모든 알람을 삭제합니다.\n"
                ":eight_spoked_asterisk: !call_in/out: 서버 텍스트 채널에서 봇을 음성 채널로 입/퇴장시킵니다."
                ":eight_spoked_asterisk: !turn_off: 디스코드 봇을 종료합니다."
            )
        elif message.content.startswith("!turn_off"):
            print("디스코드에서 봇을 종료했습니다. 좋은하루보내세요.(●'◡'●)")
            await message.channel.send("봇을 종료합니다. 좋은하루보내세요.(●'◡'●)")
            await client.close()

    except Exception as e:
        await message.author.send(f"⚠️ 오류 발생: {e}")

# ────────── 실행 ──────────
if __name__ == "__main__":
    client.run(TOKEN)
    on_message("!commend_list")