import os
import discord
from discord.ext import commands
from discord import app_commands

from myserver import server_on


# =========================
# ตั้งค่าบอท
# =========================

intents = discord.Intents.all()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================
# เมื่อบอทออนไลน์
# =========================

@bot.event
async def on_ready():
    print(f"Bot Online! : {bot.user}")

    synced = await bot.tree.sync()

    print(f"Synced {len(synced)} slash command(s)")
    print("JUZEN BOT พร้อมใช้งานแล้ว!")


# =========================
# เมื่อมีสมาชิกเข้า Server
# =========================

@bot.event
async def on_member_join(member):

    channel = bot.get_channel(1140633489520205934)

    if channel is not None:

        text = f"Welcome to the server, {member.mention}!"

        embed = discord.Embed(
            title="Welcome to the server!",
            description=text,
            color=0x66FFFF
        )

        await channel.send(text)
        await channel.send(embed=embed)

    try:
        await member.send(
            f"Welcome to the server, {member.name}!"
        )
    except discord.Forbidden:
        pass


# =========================
# เมื่อสมาชิกออกจาก Server
# =========================

@bot.event
async def on_member_remove(member):

    channel = bot.get_channel(1140633489520205934)

    if channel is not None:
        await channel.send(
            f"{member.name} has left the server!"
        )


# =========================
# ระบบอ่านข้อความ
# =========================

@bot.event
async def on_message(message):

    # ไม่ให้บอทตอบตัวเอง
    if message.author.bot:
        return

    mes = message.content.lower()

    if mes == "hello":
        await message.channel.send(
            "Hello It's me"
        )

    elif mes == "hi bot":
        await message.channel.send(
            f"Hello, {message.author.name}"
        )

    await bot.process_commands(message)


# =========================
# คำสั่ง !hello
# =========================

@bot.command()
async def hello(ctx):

    await ctx.send(
        f"hello {ctx.author.name}!"
    )


# =========================
# คำสั่ง !test
# =========================

@bot.command()
async def test(ctx, arg):

    await ctx.send(arg)


# =========================
# Slash Command /hellobot
# =========================

@bot.tree.command(
    name="hellobot",
    description="ทดสอบบอท"
)
async def hellocommand(
    interaction: discord.Interaction
):

    await interaction.response.send_message(
        "Hello It's me BOT DISCORD"
    )


# =========================
# Slash Command /name
# =========================

@bot.tree.command(
    name="name",
    description="บอกชื่อของคุณ"
)
@app_commands.describe(
    name="What's your name?"
)
async def namecommand(
    interaction: discord.Interaction,
    name: str
):

    await interaction.response.send_message(
        f"Hello {name}"
    )


# =========================
# Slash Command /help
# =========================

@bot.tree.command(
    name="help",
    description="ดูคำสั่งทั้งหมดของบอท"
)
async def helpcommand(
    interaction: discord.Interaction
):

    embed = discord.Embed(
        title="JUZEN BOT - Commands",
        description="คำสั่งที่สามารถใช้งานได้",
        color=0x66FFFF,
        timestamp=discord.utils.utcnow()
    )

    embed.add_field(
        name="/hellobot",
        value="ทดสอบว่าบอททำงานหรือไม่",
        inline=False
    )

    embed.add_field(
        name="/name",
        value="ให้บอททักชื่อ",
        inline=False
    )

    embed.add_field(
        name="/join",
        value="ให้บอทเข้าห้องเสียงที่คุณอยู่",
        inline=False
    )

    embed.add_field(
        name="/leave",
        value="ให้บอทออกจากห้องเสียง",
        inline=False
    )

    await interaction.response.send_message(
        embed=embed
    )


# =========================
# Slash Command /join
# ให้บอทเข้าห้องเสียง
# =========================

@bot.tree.command(
    name="join",
    description="ให้บอทเข้าห้องเสียงที่คุณอยู่"
)
async def joincommand(
    interaction: discord.Interaction
):

    # ตรวจสอบว่าคนใช้คำสั่งอยู่ในห้องเสียงหรือไม่
    if interaction.user.voice is None:

        await interaction.response.send_message(
            "❌ กรุณาเข้าห้องเสียงก่อน แล้วค่อยใช้ /join"
        )

        return

    # ห้องเสียงที่ผู้ใช้กำลังอยู่
    channel = interaction.user.voice.channel

    # ตรวจสอบว่าบอทอยู่ในห้องเสียงอยู่แล้วหรือไม่
    voice_client = interaction.guild.voice_client

    try:

        if voice_client is not None:

            # ถ้าบอทอยู่ห้องอื่น ให้ย้ายมาห้องของเรา
            await voice_client.move_to(channel)

        else:

            # ถ้ายังไม่ได้เข้าห้องเสียง ให้เข้า
            await channel.connect()

        await interaction.response.send_message(
            f"✅ JUZEN BOT เข้าห้อง **{channel.name}** แล้ว"
        )

    except Exception as e:

        await interaction.response.send_message(
            f"❌ ไม่สามารถเข้าห้องเสียงได้\n```{e}```"
        )


# =========================
# Slash Command /leave
# ให้บอทออกจากห้องเสียง
# =========================

@bot.tree.command(
    name="leave",
    description="ให้บอทออกจากห้องเสียง"
)
async def leavecommand(
    interaction: discord.Interaction
):

    voice_client = interaction.guild.voice_client

    if voice_client is None:

        await interaction.response.send_message(
            "❌ ตอนนี้บอทไม่ได้อยู่ในห้องเสียง"
        )

        return

    await voice_client.disconnect()

    await interaction.response.send_message(
        "👋 JUZEN BOT ออกจากห้องเสียงแล้ว"
    )


# =========================
# เริ่ม Server
# =========================

server_on()


# =========================
# TOKEN
# =========================

token = os.getenv("TOKEN")

if not token:

    raise RuntimeError(
        "TOKEN environment variable is not set"
    )


# =========================
# เปิดบอท
# =========================

bot.run(token)