import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

load_dotenv()
token = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.all()

bot = commands.Bot(command_prefix="+", intents=intents)

@bot.command()
async def say(ctx, *, message):
    await ctx.message.delete()  # supprime le message de la commande
    await ctx.send(message)
    
@bot.command()
@commands.has_permissions(manage_messages=True)
async def clear(ctx, amount: int):

    if amount < 1 or amount > 100:
        await ctx.send("Choisis un nombre entre 1 et 100.")
        return

    deleted = await ctx.channel.purge(limit=amount + 1)
    await ctx.send(f"✅ {len(deleted)-1} messages supprimés.", delete_after=3)

ROLE_ID = 1449303029202292768     # ID rôle Citoyen
MESSAGE_ID = 1477263454879486054 # ID du message
EMOJI = "✅"

@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id != MESSAGE_ID:
        return

    if str(payload.emoji) != EMOJI:
        return

    guild = bot.get_guild(payload.guild_id)
    member = guild.get_member(payload.user_id)

    if member.bot:
        return

    role = guild.get_role(ROLE_ID)

    if role not in member.roles:
        await member.add_roles(role)

@bot.command()
@commands.has_permissions(ban_members=True)  # Vérifie que l'utilisateur peut bannir
async def ban(ctx, member: discord.Member, *, reason=None):
    """Bannir un membre du serveur"""
    try:
        await member.ban(reason=reason)
        await ctx.send(f"{member} a été banni !")
    except discord.Forbidden:
        await ctx.send("Je n'ai pas la permission de bannir ce membre.")
    except discord.HTTPException:
        await ctx.send("Impossible de bannir le membre, une erreur est survenue.")

client = discord.Client(intents=discord.Intents.all())

class MonBot(commands.Bot):
    async def setup_hook(self):
        for extension in ['games', 'moderation']:
            await self.load_extension(f'cogs.{extension}')


keep_alive()
bot.run("token=token") 

if __name__ == "__main__":
    bot.run("token=token")