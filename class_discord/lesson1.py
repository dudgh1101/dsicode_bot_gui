from dotenv import load_dotenv
import os
import discord

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
dotenv_path = os.path.join(BASE_DIR, ".env")

load_dotenv(dotenv_path)
# ────────── 설정 ──────────
TOKEN = os.getenv("TOKEN")
str_commend_line=""


intents = discord.Intents.default()
intents.message_content = True
intents.members = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f"{client.user}로 로그인했습니다!")
    print(f"서버수 : {len(client.guilds)}")

@client.event
async def on_message(message):
    if message.author == client.user : return


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content == "안녕":
        await message.channel.send("안녕하세요! 👋")
    
    if message.content == "!정보":
        await message.channel.send(f"보낸 사람: {message.author}\n채널: {message.channel}")

@client.event
async def on_member_join(member):
    channel = discord.utils.get(member.guild.text_channels, name="일반")
    if channel:
        await channel.send(f"🎉 {member.mention}님 환영합니다!")
@client.event
async def on_member_remove(member):
    channel = discord.utils.get(member.guild.text_channels, name="일반")
    if channel:
        await channel.send(f"😢 {member.name}님이 나가셨습니다.")


client.run(TOKEN)


