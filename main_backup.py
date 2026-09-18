import os
import discord
from discord.ext import commands
from discord import app_commands


# =========================================================
# JUZEN BOT - ตั้งค่าหลัก
# =========================================================

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


# =========================================================
# เมื่อบอทเริ่มทำงาน
# =========================================================

@bot.event
async def on_ready():
    print("=" * 40)
    print(f"Bot Online! : {bot.user}")
    print(f"Bot ID      : {bot.user.id}")
    print("=" * 40)


# =========================================================
# Sync Slash Commands
# =========================================================

@bot.event
async def setup_hook():
    guild = discord.Object(id=1527736556478005248)

    synced = await bot.tree.sync(guild=guild)

    print(f"Synced {len(synced)} slash command(s) to JUZEN STORE")
    print("JUZEN BOT พร้อมใช้งานแล้ว!")


# =========================================================
# เมื่อสมาชิกเข้า Server
# =========================================================

@bot.event
async def on_member_join(member: discord.Member):
    # เปลี่ยนเลขนี้เป็น ID ของห้องต้อนรับของคุณ
    WELCOME_CHANNEL_ID = 1140633489520205934

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if channel is not None:
        embed = discord.Embed(
            title="Welcome to the server!",
            description=f"ยินดีต้อนรับ {member.mention} 🎉",
            color=0x66FFFF
        )

        await channel.send(
            f"Welcome to the server, {member.mention}!"
        )
        await channel.send(embed=embed)

    # ส่ง DM หาสมาชิกใหม่
    try:
        await member.send(
            f"Welcome to the server, {member.name}! 🎉"
        )
    except discord.Forbidden:
        # ผู้ใช้อาจปิดรับ DM จาก Server
        pass


# =========================================================
# เมื่อสมาชิกออกจาก Server
# =========================================================

@bot.event
async def on_member_remove(member: discord.Member):
    # เปลี่ยนเลขนี้เป็น ID ของห้องต้อนรับ/แจ้งเตือน
    WELCOME_CHANNEL_ID = 1140633489520205934

    channel = bot.get_channel(WELCOME_CHANNEL_ID)

    if channel is not None:
        await channel.send(
            f"{member.name} has left the server! 👋"
        )


# =========================================================
# ระบบอ่านข้อความ
# =========================================================

@bot.event
async def on_message(message: discord.Message):
    # ไม่ให้บอทตอบตัวเอง
    if message.author.bot:
        return

    mes = message.content.lower().strip()

    if mes == "hello":
        await message.channel.send("Hello It's me")

    elif mes == "hi bot":
        await message.channel.send(
            f"Hello, {message.author.name}"
        )

    # ทำให้คำสั่ง !hello / !test ยังใช้งานได้
    await bot.process_commands(message)


# =========================================================
# คำสั่ง !hello
# =========================================================

@bot.command()
async def hello(ctx: commands.Context):
    await ctx.send(
        f"hello {ctx.author.name}!"
    )


# =========================================================
# คำสั่ง !test
# =========================================================

@bot.command()
async def test(ctx: commands.Context, *, arg: str):
    await ctx.send(arg)


# =========================================================
# Slash Command /hellobot
# =========================================================

@bot.tree.command(
    name="hellobot",
    description="ทดสอบบอท"
)
async def hellocommand(interaction: discord.Interaction):
    await interaction.response.send_message(
        "Hello It's me JUZEN BOT 🤖"
    )


# =========================================================
# Slash Command /name
# =========================================================

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
        f"Hello {name} 👋"
    )


# =========================================================
# Slash Command /help
# =========================================================

@bot.tree.command(
    name="help",
    description="ดูคำสั่งทั้งหมดของบอท"
)
async def helpcommand(interaction: discord.Interaction):

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

    await interaction.response.send_message(embed=embed)


# =========================================================
# Slash Command /join
# ให้บอทเข้าห้องเสียงที่เราอยู่
# =========================================================

@bot.tree.command(
    name="join",
    description="ให้บอทเข้าห้องเสียงที่คุณอยู่"
)
async def joincommand(interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ คำสั่งนี้ใช้ใน Server เท่านั้น"
        )
        return

    if interaction.user.voice is None:
        await interaction.response.send_message(
            "❌ กรุณาเข้าห้องเสียงก่อน แล้วค่อยใช้ /join"
        )
        return

    channel = interaction.user.voice.channel

    if not isinstance(
        channel,
        (discord.VoiceChannel, discord.StageChannel)
    ):
        await interaction.response.send_message(
            "❌ ไม่สามารถเข้าห้องเสียงประเภทนี้ได้"
        )
        return

    # บอก Discord ก่อนว่าบอทกำลังทำงาน
    await interaction.response.defer()

    voice_client = interaction.guild.voice_client

    try:
        if voice_client is not None:
            await voice_client.move_to(channel)
        else:
            await channel.connect()

        await interaction.followup.send(
            f"✅ JUZEN BOT เข้าห้อง **{channel.name}** แล้ว"
        )

    except discord.Forbidden:
        await interaction.followup.send(
            "❌ บอทไม่มีสิทธิ์ Connect ในห้องเสียงนี้"
        )

    except Exception as e:
        await interaction.followup.send(
            f"❌ ไม่สามารถเข้าห้องเสียงได้\n```{e}```"
        )

async def joincommand(interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ คำสั่งนี้ใช้ใน Server เท่านั้น"
        )
        return

    # ตรวจสอบว่าคนใช้คำสั่งอยู่ในห้องเสียงหรือไม่
    if interaction.user.voice is None:
        await interaction.response.send_message(
            "❌ กรุณาเข้าห้องเสียงก่อน แล้วค่อยใช้ /join"
        )
        return

    channel = interaction.user.voice.channel

    # ต้องเป็น VoiceChannel หรือ StageChannel
    if not isinstance(
        channel,
        (discord.VoiceChannel, discord.StageChannel)
    ):
        await interaction.response.send_message(
            "❌ ไม่สามารถเข้าห้องเสียงประเภทนี้ได้"
        )
        return

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

    except discord.Forbidden:
        await interaction.response.send_message(
            "❌ บอทไม่มีสิทธิ์ Connect ในห้องเสียงนี้"
        )

    except Exception as e:
        await interaction.response.send_message(
            f"❌ ไม่สามารถเข้าห้องเสียงได้\n```{e}```"
        )


# =========================================================
# Slash Command /leave
# ให้บอทออกจากห้องเสียง
# =========================================================

@bot.tree.command(
    name="leave",
    description="ให้บอทออกจากห้องเสียง"
)
async def leavecommand(interaction: discord.Interaction):

    if interaction.guild is None:
        await interaction.response.send_message(
            "❌ คำสั่งนี้ใช้ใน Server เท่านั้น"
        )
        return

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


# =========================================================
# TOKEN
# =========================================================

token = os.getenv("TOKEN")

if not token:
    raise RuntimeError(
        "ไม่พบ TOKEN\n"
        "ให้ตั้งค่า TOKEN ใน Terminal ก่อนรันบอท"
    )


# =========================================================
# เปิดบอท
# =========================================================

bot.run(token)
