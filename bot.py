import os
import discord
from discord import app_commands
from discord.ext import commands
from dotenv import load_dotenv
from datetime import datetime
from zoneinfo import ZoneInfo

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("GUILD_ID", "1316621357974290472"))
CHANNEL_ID = int(os.getenv("PORTARIA_CHANNEL_ID", "0"))
CHANNEL_NAME = os.getenv("PORTARIA_CHANNEL_NAME", "Portaria")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)
guild = discord.Object(id=GUILD_ID)


async def get_portaria_channel():
    channel = bot.get_channel(CHANNEL_ID) if CHANNEL_ID else None

    if channel is None:
        channel = discord.utils.get(
            bot.get_guild(GUILD_ID).text_channels,
            name=CHANNEL_NAME
        )

    return channel


@bot.event
async def on_ready():
    await bot.tree.sync(guild=guild)
    print(f"Bot conectado como {bot.user}")
    print("Comando /teste-entrada sincronizado.")


@bot.event
async def on_member_join(member):
    if member.guild.id != GUILD_ID:
        return

    channel = await get_portaria_channel()

    if channel is None:
        print("Canal de Portaria não encontrado.")
        return

    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

    embed = discord.Embed(
        title="📥 NOVA ENTRADA NA PORTARIA",
        description=f"Bem-vindo(a), {member.mention}!",
        color=discord.Color.green(),
        timestamp=agora
    )

    embed.set_thumbnail(url=member.display_avatar.url)
    embed.add_field(name="👤 Usuário", value=member.name, inline=True)
    embed.add_field(name="🆔 ID", value=str(member.id), inline=True)
    embed.add_field(
        name="📅 Conta criada",
        value=discord.utils.format_dt(member.created_at, style="F"),
        inline=False
    )
    embed.add_field(
        name="🕒 Entrada",
        value=agora.strftime("%d/%m/%Y às %H:%M:%S"),
        inline=False
    )
    embed.set_footer(text="EB Bot • Sistema de Portaria")

    await channel.send(embed=embed)


@bot.tree.command(
    name="teste-entrada",
    description="Testa o registro de entrada na Portaria.",
    guild=guild
)
@app_commands.default_permissions(manage_guild=True)
@app_commands.checks.has_permissions(manage_guild=True)
async def teste_entrada(interaction: discord.Interaction):
    if interaction.guild_id != GUILD_ID:
        await interaction.response.send_message(
            "Este comando não está disponível neste servidor.",
            ephemeral=True
        )
        return

    channel = await get_portaria_channel()

    if channel is None:
        await interaction.response.send_message(
            "Não encontrei o canal de Portaria.",
            ephemeral=True
        )
        return

    agora = datetime.now(ZoneInfo("America/Sao_Paulo"))

    embed = discord.Embed(
        title="🧪 TESTE DE ENTRADA",
        description=f"Registro de teste solicitado por {interaction.user.mention}.",
        color=discord.Color.blue(),
        timestamp=agora
    )
    embed.set_thumbnail(url=interaction.user.display_avatar.url)
    embed.add_field(name="👤 Usuário", value=interaction.user.name)
    embed.add_field(name="🆔 ID", value=str(interaction.user.id))
    embed.set_footer(text="EB Bot • Teste da Portaria")

    await channel.send(embed=embed)
    await interaction.response.send_message(
        "Teste enviado para a Portaria!",
        ephemeral=True
    )


if not TOKEN:
    raise RuntimeError("Configure DISCORD_TOKEN no arquivo .env.")

bot.run(TOKEN)
