# Discord.py 기초 강좌

Discord 봇 만드는 방법을 단계별로 배워봅시다.

---

## 1강: 설치와 첫 실행

### 설치

터미널(명령 프롬프트)에서 다음 명령어를 입력하세요:

```bash
pip install discord.py
```

### 기본 구조

가장 간단한 Discord 봇 코드입니다:

```python
import discord

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"로그인 완료: {client.user}")

client.run("YOUR_BOT_TOKEN")
```

### 실행해보기

1. Discord Developer Portal에서 봇 토큰을 발급받으세요
2. `YOUR_BOT_TOKEN` 부분을 발급받은 토큰으로 바꾸세요
3. 실행:

```bash
python 파일이름.py
```

### 확인

실행 결과가 이렇게 나오면 성공!

```
로그인 완료: Bot이름#1234
```

---

## 2강: 이벤트 처리

Discord에서는 다양한 일이 발생할 때마다 **이벤트**가 발생합니다. 봇은 이 이벤트를 받아서 원하는 동작을 수행합니다.

### 자주 사용하는 이벤트들

| 이벤트 | 발생하는 순간 |
|--------|---------------|
| `on_ready` | 봇이 Discord에 연결되고 사용할 준비가 됐을 때 |
| `on_message` | 누군가 채팅에 메시지를 보낼 때 |
| `on_member_join` | 새 멤버가 서버에 입장할 때 |
| `on_member_remove` | 멤버가 서버를 나갈 때 |
| `on_voice_state_update` | 음성 채널 상태가 변할 때 |

### 핵심 포인트

1. **`@client.event` 데코레이터** - 이벤트를 등록할 때는 이걸 붙입니다
2. **`async def`** - 모든 이벤트 함수는 비동기(`async`)여야 합니다
3. **`return`** - 봇 자신이 보낸 메시지는 무시하려면 `if message.author == client.user: return`
4. **`intents.members = True`** - 멤버 입장/퇴장 이벤트는 이걸 설정해야 작동합니다

---

### 코드 설명 방식 (기능 + 역할 + 원리)

코드를 설명할 때는 다음 3가지를 모두 설명합니다:

#### 예시 1: `if message.author == client.user: return`

| 구분 | 설명 |
|------|------|
| **기능** | 봇 자신이 보낸 메시지를 무시하고 처리하지 않음 |
| **역할** | 무한 루프 방지. 봇이 자기 메시지에 반응 → 다시 보낸 → 또 반응 → ... 이를 막음 |
| **원리** | `message.author`는 메시지 보낸 사람 객체, `client.user`는 봇 자신의 객체. 두 값이 같으면 `return`으로 함수 즉시 종료 |

#### 예시 2: `intents.members = True`

| 구분 | 설명 |
|------|------|
| **기능** | 서버 멤버 정보에 접근할 수 있게 허용 |
| **역할** | `on_member_join`, `on_member_remove` 등 멤버 관련 이벤트가 작동하게 함 |
| **원리** | Discord는 개인정보 보호를 위해 기본적으로 멤버 정보를 숨김. `intents.members = True`로 명시적으로 허용해야 Discord API가 멤버 데이터を提供함 |

#### 예시 3: `@client.event` 데코레이터

| 구분 | 설명 |
|------|------|
| **기능** | 아래 있는 함수를 Discord 이벤트 핸들러로 등록 |
| **역할** | 특정 사건이 발생했을 때 이 함수가 자동으로 실행되게 함 |
| **원리** | 데코레이터는 함수를 감싸서 특별한 기능 добавля. `@client.event`는 Discord 라이브러리에 이 함수를 "이벤트 핸들러"라고 알려주는 역할 |

#### 예시 4: `await message.channel.send()`

| 구분 | 설명 |
|------|------|
| **기능** | 메시지를 입력한 채널에 텍스트를 보냄 |
| **역할** | 사용자 입력에 대해 답변을 보내거나 알림을 전달 |
| **원리** | `message.channel`은 메시지가 들어온 채널 객체. `send()`는 비동기 함수라 `await`로 대기해야 메시지 전송 완료 후 다음 코드 실행 |

#### 예시 5: `discord.utils.get()`

| 구분 | 설명 |
|------|------|
| **기능** | 리스트/반복가능 객체에서 조건에 맞는 첫 번째 항목 찾기 |
| **역할** | 채널 이름으로 채널 객체 찾기 |
| **원리** | `member.guild.text_channels`는 서버의 모든 텍스트 채널 리스트. `name="welcome"` 조건으로 첫 번째 매칭 채널 반환. 없으면 `None` |

---

## 3강: 명령어 만들기

가장 많이 쓰이는 "!명령어" 형식의 명령어를 만들어봅시다.

### 기본 구조

```python
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # !ping 명령어
    if message.content == "!ping":
        await message.channel.send("pong!")
    
    # !hello 명령어
    if message.content == "!hello":
        await message.channel.send(f"안녕하세요 {message.author.mention}님!")
```

### 인자가 있는 명령어

```python
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # !add 12:00 점심 이렇게 입력
    if message.content.startswith("!add "):
        parts = message.content.split(" ", 2)  # 최대 2번 분리
        if len(parts) >= 3:
            time = parts[1]
            msg = parts[2]
            await message.channel.send(f"{time}에 '{msg}' 예약됨!")
```

### 슬래시 명령어 (Slash Command)

최근에는 슬래시 명령어가 더 많이 쓰입니다:

```python
from discord import app_commands

tree = app_commands.CommandTree(client)

@tree.command()
async def ping(interaction):
    await interaction.response.send_message("pong!")

@client.event
async def on_ready():
    await tree.sync()
    print("슬래시 명령어 동기화 완료")
```

---

## 4강: 심화 기능

### 버튼 (Button)

```python
from discord.ui import Button, View

@client.event
async def on_message(message):
    if message.content == "!버튼":
        button = Button(label="클릭 me", style=discord.ButtonStyle.primary)
        
        async def button_callback(interaction):
            await interaction.response.send_message("버튼을 누르셨네요!")
        
        button.callback = button_callback
        view = View()
        view.add_item(button)
        
        await message.channel.send("아래 버튼을 눌러주세요:", view=view)
```

### 선택지 (Select)

```python
from discord.ui import Select, View

@client.event
async def on_message(message):
    if message.content == "!선택":
        select = Select(options=[
            discord.SelectOption(label="option1", description="첫 번째 선택지"),
            discord.SelectOption(label="option2", description="두 번째 선택지")
        ])
        
        async def select_callback(interaction):
            await interaction.response.send_message(f"{interaction.data['values'][0]}을 선택했네요!")
        
        select.callback = select_callback
        view = View()
        view.add_item(select)
        
        await message.channel.send("선택해주세요:", view=view)
```

---

## 5강: 음성 채널

음성 채널에 입장하고 음악을 재생하는 방법입니다.

### 음성 채널 입장

```python
@client.event
async def on_message(message):
    if message.content == "!입장":
        channel = message.author.voice.channel
        if channel:
            await channel.connect()
            await message.channel.send(f"{channel.name}에 입장했습니다!")
```

### 음성 채널 퇴장

```python
@client.event
async def on_message(message):
    if message.content == "!퇴장":
        if message.guild.voice_client:
            await message.guild.voice_client.disconnect()
            await message.channel.send("음성 채널에서 퇴장했습니다!")
```

---

## 6강: 실전 예제 - 예약 메시지 봇

지금까지 배운 내용을 합쳐서 만들어보는 예제입니다.

```python
import discord
from datetime import datetime
import pytz
import asyncio

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

user_scheduled_messages = {}

@client.event
async def on_ready():
    print(f"{client.user}로 로그인!")
    client.loop.create_task(send_scheduled_messages())

async def send_scheduled_messages():
    await client.wait_until_ready()
    channel = client.get_channel(CHANNEL_ID)
    
    seoul = pytz.timezone("Asia/Seoul")
    while not client.is_closed():
        now = datetime.now(seoul).strftime("%H:%M")
        
        for user_id, schedule in list(user_scheduled_messages.items()):
            if now in schedule:
                for msg in schedule[now]:
                    await channel.send(msg)
                del schedule[now]
        
        await asyncio.sleep(30)

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    # !add 12:00 메시지
    if message.content.startswith("!add "):
        parts = message.content.split(" ", 2)
        if len(parts) >= 3:
            time, msg = parts[1], parts[2]
            user_id = message.author.id
            user_scheduled_messages.setdefault(user_id, {}).setdefault(time, []).append(msg)
            await message.channel.send(f"{time}에 '{msg}' 예약됨!")

client.run("TOKEN")
```

---

## 중요 개념 정리

| 개념 | 설명 |
|------|------|
| **Client** | Discord 서버에 연결하는 봇
| **Event** | Discord에서 발생하는 사건 (메시지, 입장, 퇴장 등) |
| **Intents** | 봇이 어떤 정보를 받을지 설정 |
| **Message** | 채팅 메시지 |
| **Channel** | 텍스트/음성 채널 |
| **Guild** | Discord 서버 |
| **Member** | 서버 멤버 |

---

## 다음 단계

이 강의를 다 배웠다면:

1. 더 많은 명령어 만들어보기
2. 데이터베이스 연동해보기
3. 웹 dashboard 만들어보기
4. 음악 재생 봇 만들어보기

관심 있는 분야가 있으면 말씀해주세요!
