import keep_alive
keep_alive.keep_alive()

import discord
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
import json
import asyncio
import random
import time
import logging
import asyncio
from discord.errors import Forbidden
import os
import datetime

time.sleep(0.5)

print('[INFO] Loading DATA')
with open("config.json") as file: # Load the config file
    info = json.load(file)
    token = info["token"]
    prefix = info["prefix"]

time.sleep(0.5) 

print('[INFO] LOADING BOT')
bot = commands.Bot(command_prefix = prefix,intents=discord.Intents.all())
bot.remove_command("help")


time.sleep(0.5) 
print('[INFO] LOADING EVENTS')


'  The Botstart  '
@bot.event
async def on_ready():
    print(f"...time to detonate time :) [3/3]")
    print(f"Servers using {bot.user.name}:",
          len(bot.guilds))
    print("\u001b[0m")
    print("\033[94m | https://discord.com/ | \u001b[0m")
    print("\033[94m | Bot is ready | \u001b[0m")
    print(f"\033[94m | Start with +help | \u001b[0m\n")
    bot.loop.create_task(status_task(bot))


'  The Statustask  '
async def status_task(bot):
    while True:
        await bot.change_presence(activity=discord.Game(name="te regarder!"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game(name="$help"))
        await asyncio.sleep(15)
        await bot.change_presence(activity=discord.Game(name="2 serveurs | 292 membres"))
        await asyncio.sleep(15)
  
... 
@bot.command()
async def say(ctx, *texte):
	await ctx.send(" ".join(texte))

@bot.command()
async def embed(ctx, *, arg):
    embed = discord.Embed(colour =0000, description = str(arg))
    await ctx.send(embed = embed)

... 
@bot.command()
async def botstats(ctx):
  counter = 0
  for command in bot.commands:
    counter += 1
  await ctx.send(f"J'ai {counter} commandes, je suis dans {len(bot.guilds)} serveurs avec au total {len(bot.users)} membres!")
... 

@bot.command(aliases=["si"])
async def serveurinfo(ctx):
        server = ctx.guild
        id = server.id
        nbtext = len(server.text_channels)
        nbvoice = len(server.voice_channels)
        nbmember = server.member_count
        name = server.name
        embed = discord.Embed(title=f"Serveur: {name}", description=f"Membres : {nbmember}\nSalons textuels : {nbtext}\nSalons vocaux : {nbvoice}\nId : {id}", colour=0000)
        await ctx.send(embed=embed)

... 

@bot.command()
@commands.has_permissions(ban_members = True) 
async def ban(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.ban(user, reason = reason)
	await ctx.send(f"{user} à été ban pour la raison suivante : {reason}.")

@bot.command()
@commands.has_permissions(ban_members = True) 
async def unban(ctx, user, *reason):
	reason = " ".join(reason)
	userName, userId = user.split("#")
	bannedUsers = await ctx.guild.bans()
	for i in bannedUsers:
		if i.user.name == userName and i.user.discriminator == userId:
			await ctx.guild.unban(i.user, reason = reason)
			await ctx.send(f"{user} à été unban.")
			return
	#Ici on sait que lutilisateur na pas ete trouvé
	await ctx.send(f"L'utilisateur {user} n'est pas dans la liste des bans")

@bot.command()
@commands.has_permissions(ban_members = True) 
async def kick(ctx, user : discord.User, *reason):
	reason = " ".join(reason)
	await ctx.guild.kick(user, reason = reason)
	await ctx.send(f"{user} à été kick.")

@bot.command(aliases = ['purge', 'delete'])
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount: int = 1000000):
    await ctx.channel.purge(limit = amount)


... 
@bot.command(aliases=["ping"])
async def latency(ctx):
	if int(round(bot.latency * 1000)) <= 50:
		color=0x000000
	elif int(round(bot.latency * 1000)) <= 100:
		color=0x00FF00
	elif int(round(bot.latency * 1000)) <= 300:
		color=0x00FFFF
	else:
		color=0xFF0000
	if ctx.message.content.lower().startswith(f"{bot.command_prefix}latency"):
		title="Latency"
	elif ctx.message.content.lower().startswith(f"{bot.command_prefix}ping"):
		title="Ping"
	else:
		title="Latency"
	hehe = discord.Embed(title=title,description=f"Latency : {str(round(bot.latency * 1000))}ms", color=color)
	await ctx.send(embed=hehe)
...

@bot.command()
async def credits(ctx):
	await ctx.send("Créateur: Felosi Support: https://discord.gg/5wKDaYWs9p")

... 
@bot.command(aliases=["cmr"])
@commands.has_permissions(ban_members = True) 
async def createMutedRole(ctx):
    mutedRole = await ctx.guild.create_role(name = "Muted",
                                            permissions = discord.Permissions(
                                                send_messages = False,
                                                speak = False),
                                            reason = "Creation du role Muted pour mute des gens.")
    for channel in ctx.guild.channels:
        await channel.set_permissions(mutedRole, send_messages = False, speak = False)
    return mutedRole

async def getMutedRole(ctx):
    roles = ctx.guild.roles
    for role in roles:
        if role.name == "Muted":
            return role
    
    return await createMutedRole(ctx)

@bot.command()
@commands.has_permissions(ban_members = True) 
async def mute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.add_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été mute !")

@bot.command()
@commands.has_permissions(ban_members = True) 
async def unmute(ctx, member : discord.Member, *, reason = "Aucune raison n'a été renseigné"):
    mutedRole = await getMutedRole(ctx)
    await member.remove_roles(mutedRole, reason = reason)
    await ctx.send(f"{member.mention} a été unmute !")

... 
 
@bot.command()
async def help(ctx):
    '''Envoie la liste des commandes et leurs fonctions'''
    embed = discord.Embed(colour=discord.Colour.blue())
    embed.set_author(name="LISTE DES COMMANDES")
  
  
    embed.add_field(name="**$help**", value="Montre ce message", inline=False)
    embed.add_field(name="**$clear**", value="Efface des messages", inline=False)
    embed.add_field(name="**$ban**", value="Ban un membre", inline=False)
    embed.add_field(name="**$unban**", value="Unban un membre", inline=False)
    embed.add_field(name="**+kick**", value="Expulse un membre", inline=False)
    embed.add_field(name="**$cmr**", value="Créé le role mute", inline=False)
    embed.add_field(name="**$mute**", value="Mute un membre du serveur", inline=False)
    embed.add_field(name="**$unmute**", value="Unmute un membre du serveur", inline=False)
    embed.add_field(name="**$serveurinfo**", value="Montre les infos du serveur", inline=False)
    embed.add_field(name="**$ping**", value="Montre la latence du bot", inline=False)
    embed.add_field(name="**$say**", value="Le bot va envoyer le message que vous voulez", inline=False)
    embed.add_field(name="**$embed**", value="Le bot va envoyer le message que vous voulez en embed", inline=False)
    embed.add_field(name="**$avatar**", value="Montre l'image de profil d'un membre", inline=False)
    embed.add_field(name="**$credits**", value="Montre les credits", inline=False)
    embed.add_field(name="**$kill**", value="Tue un membre du serveur", inline=False)
    embed.add_field(name="**$hug**", value="Donne un calin à un membre du serveur", inline=False)
    embed.add_field(name="**$kiss**", value="Embrasse un membre du serveur", inline=False)
    embed.add_field(name="**$giveaway**", value="Créé un giveaway (en secondes)", inline=False)
    embed.add_field(name="**$botstats**", value="Voir le nombre total de serveurs et de membres", inline=False)
    embed.add_field(name="**$wlc**", value="Souhaite la bienvenue à un nouveau membre", inline=False)
    embed.add_field(name="**$lock**", value="Lock un salon", inline=False)
    embed.add_field(name="**$unlock**", value="Unlock un salon", inline=False)
    embed.add_field(name="**$update**", value="Télécharge les nouvelles commandes/mises à jours", inline=False)
    embed.add_field(name="**$minesweeper**", value="Joue au jeu de déminage", inline=False)
    await ctx.send(embed=embed) 

... 
@bot.command(pass_context=True)
async def kill(ctx, member: discord.Member):



    kill = 'https://cdn.discordapp.com/attachments/769919082471620628/769942090309959690/gif_kill_1.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769942149948506152/gif_kill_2.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769942430967136266/gif_kill_3.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769942443490803762/gif_kill_4.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769942608583327754/gif_kill_5.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769942737189339146/gif_kill_7.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769943963439464528/git_kill_8.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769944073527754792/git_kill_9.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769944174023278612/git_kill_10.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769944265877880862/git_kill_11.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769944355535847434/git_kill_12.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769944420765401118/git_kill_13.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769944495260565524/git_kill_14.gif', 'https://cdn.discordapp.com/attachments/769919082471620628/769944557622132776/git_kill_15.gif'
    embed = discord.Embed(
        description=f'{ctx.message.author.mention} a tué {member.mention}  !',
        color=discord.Colour.blue()
    )
    embed.set_image(
        url=random.choice(kill))
    embed.set_footer(text='GamerBot')
    await ctx.send(embed=embed)


@bot.command(pass_context=True)
async def kiss(ctx, member: discord.Member):



    kiss = 'https://giphy.com/embed/eB5yNubYUlVoNWCIQZ', 'https://cdn.discordapp.com/attachments/765278564123017246/769852722534154260/gif_kiss_1.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769852806646464512/gif_kiss_2.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769853047965745162/gif_kiss_4.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769853143223369728/gif_kiss_5.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769853264089972756/gif_kiss_6.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769853338334134282/gif_kiss_7.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769853440889061417/gif_kiss_8.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769853541049172013/gif_kiss_9.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769853607859191808/gif_kiss_10.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769853722171539466/gif_kiss_11.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769854252356861952/gif_kiss_12.gif', 'https://cdn.discordapp.com/attachments/765278564123017246/769854334904959016/gif_kiss_13.gif'
    embed = discord.Embed(
        description=f' {ctx.message.author.mention} a donné un bisous à {member.mention} !',
        color=discord.Colour.blue()
    )
    embed.set_image(
        url=random.choice(kiss))
    embed.set_footer(text='GamerBot')
    await ctx.send(embed=embed)



@bot.command(pass_context=True)
async def hug(ctx, member: discord.Member):



    hugs = 'https://cdn.discordapp.com/attachments/764417825795866625/769844384156876830/hug_gif_1.gif', 'https://cdn.discordapp.com/attachments/764417825795866625/769844704635781160/hug_gif_2.gif', 'https://acegif.com/wp-content/gif/anime-hug-38.gif', 'https://cdn.discordapp.com/attachments/764417825795866625/769845192152842250/hug_gif_3.gif', 'https://cdn.discordapp.com/attachments/764417825795866625/769845712179167262/hug_gif_4.gif', 'https://cdn.discordapp.com/attachments/764417825795866625/769845864591261706/hug_gif_5.gif', 'https://i.imgur.com/nrdYNtL.gif', 'https://i.imgur.com/v47M1S4.gif', 'https://i.imgur.com/4oLIrwj.gif'
    embed = discord.Embed(
        description=f' {ctx.message.author.mention} a donné un câlin à {member.mention}  !',
        color=discord.Colour.blue()
    )
    embed.set_image(
        url=random.choice(hugs))
    embed.set_footer(text='GamerBot')
    await ctx.send(embed=embed)

... 

print('[INFO] CONNECTING TO API')

... 
@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.CommandNotFound):
		await ctx.send("Mmmmmmh, j'ai bien l'impression que cette commande n'existe pas :/")

	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Il manque un argument.")
	elif isinstance(error, commands.MissingPermissions):
		await ctx.send("Vous n'avez pas les permissions pour faire cette commande.")
	elif isinstance(error, commands.CheckFailure):
		await ctx.send("Oups vous ne pouvez iutilisez cette commande.")
	if isinstance(error.original, discord.Forbidden):
		await ctx.send("Oups, je n'ai pas les permissions nécéssaires pour faire cette commmande") 

  
... 

@bot.command()
async def avatar(ctx, *,  avamember : discord.Member=None):
    userAvatarUrl = avamember.avatar_url
    await ctx.send(userAvatarUrl)
... 

@bot.command(pass_context=True)
async def wlc(ctx, member: discord.Member):
    embed=discord.Embed(title="Bienvenue!",description=f"{member.mention} passe un bon moment sur le serveur! ")
    color=discord.Colour.blue()

    embed.set_image(
        url=("https://c.tenor.com/bb_M2me33L8AAAAC/sakura-cherry-blossoms.gif"))
    await ctx.send(embed=embed)


... 
@bot.listen()
async def on_message(message):
    msg = message.content
    user = message.author
    if user == bot.user :
        return
    if message.content ==  ('Salut'):
     await message.add_reaction("👋")
      
... 

@bot.command()
@has_permissions(manage_channels=True)
async def lock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role,send_messages=False)
    await ctx.send( ctx.channel.mention + " ***est maintenant fermé.***")

@bot.command()
@has_permissions(manage_channels=True)
async def unlock(ctx):
    await ctx.channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(ctx.channel.mention + " ***est maintenant ouvert.***")

... 

@bot.command(aliases=["download"])
async def update(ctx):
 await ctx.send("Téléchargement des mises à jour....")
 await ctx.send("Mise à jour aux 50 serveurs. Dernière version **v2.0.1**.")
 await ctx.send("Redémarrage...")
 await ctx.send("Bot en ligne.")
  
... 

@bot.command()
async def minesweeper(ctx):
    await ctx.send("💣 Minesweeper 💣")
    await ctx.send("||:zero:|| ||:zero:|| ||:zero:|| ||:zero:|| ||:zero:|| ||:zero:|| ||:zero:|| ||:zero:|| ||:zero:||")
    await ctx.send("||:zero:|| ||:one:|| ||:one:|| ||:one:|| ||:zero:|| ||:zero:|| ||:one:|| ||:two:|| ||:two:||")
    await ctx.send("||:zero:|| ||:one:|| ||:boom:|| ||:one:|| ||:one:|| ||:one:|| ||:two:|| ||:boom:|| ||:boom:||")
    await ctx.send("||:one:|| ||:two:|| ||:two:|| ||:two:|| ||:two:|| ||:boom:|| ||:two:|| ||:three:|| ||:three:||")
    await ctx.send("||:one:|| ||:boom:|| ||:one:|| ||:one:|| ||:boom:|| ||:two:|| ||:one:|| ||:one:|| ||:boom:||")
    await ctx.send("||:one:|| ||:one:|| ||:one:|| ||:one:|| ||:two:|| ||:two:|| ||:one:|| ||:one:|| ||:one:||")
    await ctx.send("||:one:|| ||:one:|| ||:one:|| ||:zero:|| ||:two:|| ||:boom:|| ||:two:|| ||:zero:|| ||:zero:||")
    await ctx.send("||:one:|| ||:boom:|| ||:one:|| ||:zero:|| ||:two:|| ||:boom:|| ||:two:|| ||:zero:|| ||:zero:||")
    await ctx.send("||:one:|| ||:one:|| ||:one:|| ||:zero:|| ||:one:|| ||:one:|| ||:one:|| ||:zero:|| ||:zero:||")
    await ctx.send("1️⃣,2️⃣,3️⃣ = points et 💥 = bombe qui vous fait perdre la partie")

... 
bot.run("LE TOKEN DE VOTR BOT")  