from discord.ext import commands
from os import system
import discord,random,string
from pyfiglet import figlet_format
from main_functions.ui_functions import paint,hour
from main_functions.tokencheck import check_token
from requests import session, post
from base64 import b64encode
from aiohttp import ClientSession
from io import BytesIO
from datetime import datetime

token = "token"
prefix = '-'
err = f"{paint((255,0,0), 'ERROR  ')}" 
suc = f"{paint((68,214,44), 'SUCCESS')}"
whitelisted_users = []

bot = commands.Bot(command_prefix=prefix,self_bot=True, help_command=None)

@bot.event
async def on_ready():
    system('cls')
    token_statut = check_token(token)
    system('title Lerisk V1.0.0 by krx')
    print(f'''
─────────┤lerisk aggravé├─────────

Token status       : {paint((204,204,0), token_statut)}

Connected to user  : {paint((204,204,0), bot.user.name+'#'+bot.user.discriminator)}
Bot prefix         : {paint((204,204,0), prefix)}
''')

@bot.command()
async def cmd(ctx):
    await ctx.message.delete()
    await ctx.send("""```
Lerisk selfbot by > krx#5550

+--------------[functional]--------------+
clear() amount
sclear() amount
unwhitelist unwl user
whitelist() wl user
restart
ban() user reason
kick() user reason

+---------------[utility]---------------+
avatar() av user
get_half_token() tok user
encode_base64() message
serverinfo() si

+----------------[misc]----------------+
hypesquad() hs house
ascii() message
massreaction() mr amount emote
streaming() str message
watching() wat message
playing() ply message
listening() lis message
stop_activity() stopa
wordreaction() wr word
spamreaction() sr
spam() s amount message
ghostping() gp message
generate_fake_token() ftok user
```""")
    
@bot.command()
async def sclear(ctx, amount : int):
    await ctx.message.delete()
    try:
        messages = await ctx.channel.history(limit = amount + 1).flatten()
        for message in messages:
            if str(message.author) == str(bot.user.name+'#'+bot.user.discriminator):
                try:
                    await message.delete()
                except:
                    pass
        print(f"[{hour()}] {suc} - Deleted {amount} messages from {str(bot.user.name+'#'+bot.user.discriminator)}.")
    except:
        print(f"[{hour()}] {err} - Failed to delete {amount} messages from {str(bot.user.name+'#'+bot.user.discriminator)}.")

@bot.command()
async def delete(ctx):
    await ctx.message.delete()
    channel = ctx.message.channel
    async for sent_message in channel.history():
        if sent_message.author == ctx.message.author:
            try:
                await sent_message.delete()
            except:
                await (sent_message+1).delete()
                pass

@bot.command(aliases=['b64'])
async def encode_base64(ctx, msg: str):
    await ctx.message.delete()
    msg = str(b64encode('{}'.format(msg).encode('ascii')))
    enc = msg[2:len(msg)-1]
    await ctx.send(enc)

@bot.command()
async def ban(ctx, member = discord.Member, *, reason = None):
    await ctx.message.delete()
    try:   
        await member.ban(reason = reason)
        print(f"[{hour()}] {suc} - Banned member {discord.member} reason : {reason}.")
    except:
        print(f"[{hour()}] {err} - Unable to ban member {discord.member}, no permissions ?.")
    
@bot.command()
async def kick(ctx, member = discord.Member, *, reason = None):
    await ctx.message.delete()
    try:   
        await member.kick(reason = reason)
        print(f"[{hour()}] {suc} - Kicked member {discord.member} reason : {reason}.")
    except:
        print(f"[{hour()}] {err} - Unable to kick member {discord.member}, no permissions ?.")

@bot.command(aliases=['tok'])
async def get_half_token(ctx, user: discord.User = None):
    await ctx.message.delete()
    if discord.User != None:
        try:
            msg = str(b64encode('{}'.format(user.id).encode('ascii')))
            enc = msg[2:len(msg)-1]
            await ctx.send(enc)
            print(f"[{hour()}] {suc} - Sent {discord.User} half token.")
        except discord.User == None:
            print(f"[{hour()}] {err} - Failed to fetch half token from {discord.User}.")
    else:
        print(f"[{hour()}] {err} - Failed to fetch half token from {discord.User}, no user specified ?")

@bot.command(aliases=['ftok'])
async def generate_fake_token(ctx, user: discord.User = None):
    await ctx.message.delete()
    if discord.User != None:
        try:
            msg = str(b64encode('{}'.format(user.id).encode('ascii')))
            fake_token = (msg[2:len(msg)-1]).replace('=', '')
            await ctx.send(f'{fake_token}.{random_string(6)}.{random_string(27)}')
            print(f"[{hour()}] {suc} - Sent fake token for {discord.User}.") 
        except:
            print(f"[{hour()}] {err} - Failed to send fake token for {discord.User}.")
    else:
        print(f"[{hour()}] {err} - Failed to send fake token for {discord.User}, no user specified ?")

@bot.command(aliases=['gp'])
async def ghostping(ctx, message):
    try:
        await ctx.message.delete()         
        print(f"[{hour()}] {suc} - Ghostpinged {message}.")
    except:
        print(f"[{hour()}] {err} - Failed to ghostping.")

@bot.command(aliases=['av'])
async def avatar(ctx, user: discord.User = None):
    await ctx.message.delete()
    try:
        format = "gif"
        user = user or ctx.author
        if user.is_avatar_animated() != True:
            format = "png"
        avatar = user.avatar_url_as(format=format if format != "gif" else None)
        async with ClientSession() as session:
            async with session.get(str(avatar)) as resp:
                image = await resp.read()
        with BytesIO(image) as file:
            await ctx.send(file=discord.File(file, f"Avatar.{format}"))
        print(f"[{hour()}] {suc} - Sent avatar from {discord.User}.")
    except:
        print(f"[{hour()}] {err} - Failed to send avatar from {discord.User}.")
        
@bot.command()
async def clear(ctx, amount: int):
    await ctx.message.delete()
    try:
        messages = await ctx.channel.history(limit = amount + 1).flatten()
        for message in messages:
            await message.delete()
        print(f"[{hour()}] {suc} - Deleted {amount} messages in {ctx.channel}.")
    except:
        print(f"[{hour()}] {err} - Failed to delete {amount} messages in {ctx.channel}.")

@bot.command(aliases=['sr'])
async def spamreaction(ctx):
    await ctx.message.delete()
    emotes = ['🔱','🐒','🕵️','🐛','😂','🥵','🥶','🎃','💀','🤡','🧠','👑','💻','🏴‍☠️','🏆','🏴','🔞','🏳️','🛺','☀️']
    try:
        messages = await ctx.message.channel.history(limit=1).flatten()
        for message in messages:
            for emote in emotes:
                await message.add_reaction(emote)
        print(f"[{hour()}] {suc} - Spammed '{messages[0].content}' with max reactions.")
    except:
        print(f"[{hour()}] {err} - Failed to add max reactions on '{messages[0].content}'.")
            
@bot.command(aliases=["si"])
async def serverinfo(ctx):
    await ctx.message.delete()
    date_format = "%a, %d %b %Y %I:%M %p"
    try:
        await ctx.send(f"""```
Server name     : {ctx.guild.name}
Server creation : {ctx.guild.created_at.strftime(date_format)}
Server Owner    : <@{ctx.guild.owner_id}>
Server ID       : {ctx.guild.id}
Members         : {ctx.guild.member_count}
Roles           : {len(ctx.guild.roles)}
Text-Channels   : {len(ctx.guild.text_channels)}
Voice-Channels  : {len(ctx.guild.voice_channels)}
Categories      : {len(ctx.guild.categories)}
```""")
        print(f"[{hour()}] {suc} - Retrieved infos for current server : {ctx.guild.name}.")
    except AttributeError:
        print(f"[{hour()}] {err} - Can't retrieve infos from dms, use command in a server.")

@bot.command(aliases=['wr'])
async def wordreaction(ctx, *,word: str):
    await ctx.message.delete()
    emotes_letters = {'🇦':'a','🇧':'b','🇨':'c','🇩':'d','🇪':'e','🇫':'f','🇬':'g','🇭':'h','🇮':'i','🇯':'j','🇰':'k','🇱':'l','🇲':'m','🇳':'n','🇴':'o','🇵':'p','🇶':'q','🇷':'r','🇸':'s','🇹':'t','🇺':'u','🇻':'v','🇼':'w','🇽':'x','🇾':'y','🇿':'z'}
    letters = []
    for w in word:
        letters.append(w)
    messages = await ctx.message.channel.history(limit=1).flatten()
    try:
        for message in messages:
            for letter in letters:
                for emlet in emotes_letters:
                    if emotes_letters[emlet] == letter:
                        await message.add_reaction(emlet)
        print(f"[{hour()}] {suc} - Reactions were added to make word : {word}")
    except:
        print(f"[{hour()}] {err} - Unable to add emotes to message.")

@bot.command(aliases=['str'])
async def streaming(ctx, *, message):
    try:
        await ctx.message.delete()
        stream = discord.Streaming(
            name = message,
            url = "https://www.twitch.tv/lerisk", 
        )
        await bot.change_presence(activity=stream)
        print(f"[{hour()}] {suc} - Streaming activity was set to : {message}")
    except:
        print(f"[{hour()}] {err} - Unable to set streaming to : {message}") 

@bot.command(aliases=['ply'])
async def playing(ctx, *, message):
    try:
        await ctx.message.delete()
        game = discord.Game(
            name=message
        )
        await bot.change_presence(activity=game)
        print(f"[{hour()}] {suc} - Playing activity was set to : {message}")
    except:
        print(f"[{hour()}] {err} - Unable to set playing to : {message}")

@bot.command(aliases=['lis'])
async def listening(ctx, *, message):
    try:
        await ctx.message.delete()
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening, 
                name=message, 
            ))
        print(f"[{hour()}] {suc} - Listening activity was set to : {message}")
    except:
        print(f"[{hour()}] {err} - Unable to set listening to : {message}")
      
@bot.command(aliases=['wat'])
async def watching(ctx, *, message):
    try:
        await ctx.message.delete()
        await bot.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.watching, 
                name=message
            ))
        print(f"[{hour()}] {suc} - Watching activity was set to : {message}")
    except:
        print(f"[{hour()}] {err} - Unable to set watching to : {message}")
@bot.command(aliases=['stopa'])
async def stop_activity(ctx):
    try:
        await ctx.message.delete()
        await bot.change_presence(activity=None, status=discord.Status.dnd)
        print(f"[{hour()}] {suc} - Status activity was stopped.")
    except:
        print(f"[{hour()}] {err} - Unable to stop activity.")

@bot.command(aliases=['mr'])
async def massreaction(ctx, amount: int, emote: str):
    await ctx.message.delete()
    messages = await ctx.message.channel.history(limit=amount).flatten()
    try:
        for message in messages:
            await message.add_reaction(emote)
        print(f"[{hour()}] {suc} - All the emotes were added to message.")
    except:
        print(f"[{hour()}] {err} - Unable to add emotes to message.")

@bot.command()
async def restart(ctx):
    await ctx.message.delete()
    system('start.bat')
    exit()

@bot.command()
async def afk(ctx, status: str = None, *, reason: str = None):
    await ctx.message.delete()
    is_afk = False
    if status == 'on':
        is_afk = True
        if reason == None:
            reason = 'Just wait.'
        stream = discord.Streaming(
            name = reason,
            url = "https://www.twitch.tv/lerisk", 
        )
        await bot.change_presence(activity=('afk : ',stream))
        print(f"[{hour()}] {suc} - Set afk mode with reason : {reason}.")
    elif status == 'off':
        is_afk = False
        await bot.change_presence(activity=None, status=discord.Status.dnd)
        print(f"[{hour()}] {suc} - Disabled afk mode.")
    elif status == None:
        print(f"[{hour()}] {err} - No status provided, add on / off to command.")
    

@bot.command()
async def ascii(ctx, *, args: str):
    await ctx.message.delete()
    try:
        text = figlet_format(args)
        await ctx.send(f'```{text}```')
        print(f"[{hour()}] {suc} - Sent ascii text : {args}.")
    except:
        print(f"[{hour()}] {err} - Failed to send ascii text.")

@bot.command(aliases=['wl'])
async def whitelist(ctx, user: discord.User = None):
    if user != None:
        whitelisted_users.append(user.id)
        print(f"[{hour()}] {suc} - User has been added to the whitelist.")
    else:
        print(f"[{hour()}] {err} - Unable to add user to the whitelist, no user specified ?")

@bot.command(aliases=['s'])
async def spam(ctx, amount: int, *, message):
    await ctx.message.delete()
    try:
        for i in range(0,amount):
            await ctx.send(message)
        print(f"[{hour()}] {suc} - Sent {message} {amount}x.")
    except:
        print(f"[{hour()}] {err} - Unable to spam message : {message}")

@bot.command(aliases=['unwl'])
async def unwhitelist(ctx, user: discord.User = None):
    print(whitelisted_users)
    if user != None:
        whitelisted_users.remove(user.id)
        print(f"[{hour()}] {suc} - User has been deleted from the whitelist.")
    else:
        print(f"[{hour()}] {err} - Unable to delete user from the whitelist, no user specified ?")

@bot.command(aliases=['hs'])
async def hypesquad(ctx, house):
    await ctx.message.delete()
    request = session()
    headers = {
        'Authorization': token,
        'Content-Type': 'application/json'
    }
    payload = ''
    if house == "bravery" or house == "bra":
        payload = {'house_id': 1}
        house = 'bravery'
    elif house == "brilliance" or house == "bri":
        payload = {'house_id': 2}
        house = 'brilliance'
    elif house == "balance" or house == "bal":
        payload = {'house_id': 3}
        house = 'balance'
    else:
        print(f"[{hour()}] {err} - {house} isn't a valid house.")
        payload = 'invalid'
    if payload != 'invalid':    
        try:
            post('https://discordapp.com/api/v6/hypesquad/online', headers=headers, json=payload)
            print(f"[{hour()}] {suc} - Hypesquad house was set to {house}.")
        except:
            print(f"[{hour()}] {err} - Unable to set hypesquad house to {house}.")

@bot.listen()
async def on_message(message):
    if prefix in str(message.content):
        for whitelisted_user in whitelisted_users:
            if str(message.author.id) == str(whitelisted_user):
                print('author test passed')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        print(f"[{hour()}] {err} - Missing an argument.")
    if isinstance(error, commands.MissingPermissions):
        print(f"[{hour()}] {err} - Missing some permissions.")

@bot.event
async def on_message_edit(before, after):
    await bot.process_commands(after)

def random_string(max):
    return "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase) for i in range(0,max))

bot.run(token, bot=False)