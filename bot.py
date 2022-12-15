# bot.py
import os
import random
import discord
import platform
import urllib.parse as p

from discord.ext import commands, tasks
from googleapiclient.discovery import build
from yapi import yApi

TOKEN = os.environ['DISCORD_TOKEN']
PREFIX = os.environ['PREFIX']
OWNER_ID = os.environ['OWNER_ID']
DEVELOPER_KEY = os.environ['DEVELOPER_KEY']

def youtube_authenticate():
    api_service_name = "youtube"
    api_version = "v3"
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    return build(api_service_name, api_version, developerKey=DEVELOPER_KEY)

youtube = youtube_authenticate()
bot = commands.Bot(command_prefix=PREFIX, intents=discord.Intents.all())

@bot.event
async def on_ready() -> None:
    """
    The code in this even is executed when the bot is ready
    """
    print(f"Logged in as {bot.user.name}")
    print(f"discord.py API version: {discord.__version__}")
    print(f"Python version: {platform.python_version()}")
    print(f"Running on: {platform.system()} {platform.release()} ({os.name})")
    print(f"Auth with youtube" if youtube else f"No auth with youtube")
    print("-------------------")
    status_task.start()

@tasks.loop(minutes=1.0)
async def status_task() -> None:
    """
    Setup the game status task of the bot
    """
    
    statuses = ["with you!", "with Krypton!", "with humans!"]
    await bot.change_presence(activity=discord.Game(random.choice(statuses)))

@bot.event
async def on_command_completion(context: commands.Context) -> None:
    """
    The code in this event is executed every time a normal command has been *successfully* executed
    :param context: The context of the command that has been executed.
    """
    
    full_command_name = context.command.qualified_name
    split = full_command_name.split(" ")
    executed_command = str(split[0])
    
    if context.guild is not None:
        print(
            f"Se ejecuto el comando {executed_command} en {context.guild.name} (ID: {context.guild.id}) por {context.author} (ID: {context.author.id})")
    else:
        print(
            f"Se ejecuto el comando {executed_command} por {context.author} (ID: {context.author.id}) en DMs")
        
@bot.event
async def on_command_error(context: commands.Context, error: Exception) -> None:
    """
    The code in this event is executed every time a normal valid command catches an error
    :param context: The context of the normal command that failed executing.
    :param error: The error that has been faced.
    """   
     
    if isinstance(error, commands.MissingPermissions):
        embed = discord.Embed(
            title="Error!",
            description="Necesitas los permisos: `" + ", ".join(
                error.missing_permissions) + "` para ejecutar este comando!",
            color=0xE02B2B
        )
        await context.send(embed=embed)
        
    elif isinstance(error, commands.MissingRequiredArgument):
        embed = discord.Embed(
            title="Error!",
            description='No has ingresado argumentos.',
            color=0xE02B2B
        )
        await context.send(embed=embed)
    
    elif isinstance(error, commands.CommandInvokeError):
        embed = discord.Embed(
            title="Error!",
            description=error.__cause__,
            color=0xE02B2B
        )
        await context.send(embed=embed)
    
    raise error

@bot.command()
async def yvideo(ctx: commands.Context, video_url: str):
    parsed_url = p.urlparse(video_url)
    video_id = p.parse_qs(parsed_url.query).get('v')
        
    if video_id:
         pass
    else:
        raise Exception('¡Link inválido!')
        
    video_data_api = yApi(youtube=youtube, parts=('snippet','contentDetails','statistics'))
    
    ysnippets = video_data_api.get_video_data(id=video_id).get('items')[0]['snippet']
    ystatistics = video_data_api.get_video_data(id=video_id).get('items')[0]['statistics']
    
    title, description, channelId, publishedAt, channelTitle = map(ysnippets.get, ('title', 'description', 'channelId', 'publishedAt', 'channelTitle'))
    likeCount, viewCount, commentCount = map(ystatistics.get, ('likeCount', 'viewCount', 'commentCount'))
    
    
    embed = discord.Embed(
            title=f'{(title)}',
            description=description,
            color=0x2ECC71,
        )
    embed.set_author(url=f'https://www.youtube.com/channel/{channelId}', name=channelTitle)
    embed.set_footer(text=publishedAt)
    embed.add_field(name="Número de likes:", value=likeCount, inline=True)
    embed.add_field(name="Número de comentarios:", value=commentCount, inline=True)
    embed.add_field(name="Número de visitas", value=viewCount, inline=True)
    embed.set_image(url=ysnippets["thumbnails"]["maxres"]["url"])
    
    await ctx.send(embed=embed)

@bot.command()
async def svideo(ctx: commands.Context, *param: str):
    param = ' '.join(param)
    search_data_api = yApi(youtube=youtube, parts=('snippet', ))
    video_data_api = yApi(youtube=youtube, parts=('snippet', 'statistics'))

    youtube_data_search = search_data_api.get_search_data(q=param, maxResults=6)
    items = youtube_data_search.get('items')
    
    embed = discord.Embed(
            title=f'Busqueda: {param}',
            color=0x2ECC71
        )
    
    for item in items:
        id = item['id']
        video_id = id.get('videoId')
        
        if video_id is None:
            continue
            
        youtube_data_video_snippet = video_data_api.get_video_data(id=video_id).get('items')[0]['snippet']
        
        title, publishedAt, channelTitle = map(youtube_data_video_snippet.get, ('title', 'publishedAt', 'channelTitle'))
        embed.add_field(name=f"Video: https://www.youtube.com/watch?v={video_id}", 
                        value=f'*Titulo:* {title}\n*Canal:* {channelTitle}\n*Fecha de publicacion:* {publishedAt}', inline=False)
    
    await ctx.send(embed=embed)

bot.run(TOKEN)

