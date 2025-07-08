from .classes.Server import Server
from .classes.User import User
from .classes.Shop import *
from .classes.Views import *

from typing import Any, Literal
import discord, os, random, asyncio, math, unicodedata
from discord.ext import commands
from JPyDB import pyDatabase, Tables

Economy_Color = 0x00FF00
Level_Color = 0x33daff
Debug_Color = 0x000000
Funny_Color = 0xecff33

intents = discord.Intents.default()
intents.moderation = True

pdb =pyDatabase('./data/database')

owner_ids:list[int,] = [int(x) for x in os.environ.get('OWNER').split(',')]

tips = [
    'Dinheiro no banco não pode ser roubado',
    'Donos dos servidores podem definir o imposto sobre transações',
    'Quanto maior sua reputação, mais experiência e dinheiro você ganha',
    'Alguns itens desbloqueiam comandos'
]
def getUser(client,user_id:int) -> User:
    if client.db.findByText('users', 'id', user_id)['id'] != None:
        u = User(user_id,client).load(client.db.findByText('users', 'id', user_id)['data_user'])
    else:
        u = User(user_id, client)
        client.db.add_values('users', ['id', 'data_user'], [user_id, u.save()] , user_id)
        client.db.save()
    return u
    
def getServer(client,server_id:int) -> Server:
    if client.db.findByText('servers', 'id', server_id)['id'] != None:
        s = Server(server_id).load(client.db.findByText('servers', 'id', server_id)['data_server'])
    else:
        s = Server(server_id)
        client.db.add_values('servers', ['id', 'data_server'], [server_id, s.save()], server_id)
        client.db.save()
    return s

def normalize_text(text:str) -> str:
    return unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')


def humanize_number(value:float) -> str:
    # 1000 -> 1k
    # 10000 -> 10k
    # 100000 -> 100k
    # 1000000 -> 1M
    # 10000000 -> 10M
    # 100000000 -> 100M
    # ...
    suffixes = ['', 'k', 'M', 'B', 'T','Qd']
    i = 0
    while abs(value) >= 1000 and i < len(suffixes) - 1:
        value /= 1000
        i += 1
    return f"{value:.2f}{suffixes[i]}"

class Bot(discord.Client):
    synced:bool = False
    def __init__(self, *, intents: discord.Intents, **options: Any) -> None:
        super().__init__(intents=intents, **options)
        self.synced = False
        self.db = pdb.database
        if not ('servers' in self.db.tables.keys()):
            self.db.create_table('servers', [('id',int), ('data_server',bytes)])
        if not ('users' in self.db.tables.keys()):
            self.db.create_table('users', [('id', int), ('data_user', bytes)])
        self.db.save()

    def getUser(self,user_id:int) -> User:
        return getUser(self,user_id)
    
    def getServer(self,server_id:int) -> Server:
        return getServer(self,server_id)

    def humanize_cash(self,cash:int) -> str:
        return self.humanize_number(cash)
    def humanize_number(self, value:float) -> str:
        return humanize_number(value)
    
    async def loop_Status(self):
        await self.wait_until_ready()

        status = [
            'NineSix 🇧🇷', 'Olá!', 'Apenas uma Aplicação do Discord!', 'Bot Desenvolvido em Python'
        ]
        last = ''
        while not self.is_closed():
            stats = random.choices(status)[0]
            if stats == last:
                while stats == last:
                    stats = random.choices(status)[0]
            await self.change_presence(activity=discord.Game(name=stats))
            await asyncio.sleep(10)
            last = stats
    async def on_ready(self):
        try:
            if not self.synced:
                await t.sync()
                self.synced = True
                print('Synced CommandTree!')
        except: pass
        print(f"""
              Logged in as {self.user}!
              """)
        self.loop.create_task(self.loop_Status())
    
    async def on_message(self, message:discord.Message):
        if message.author != self.user and message.author.bot == False:
            server = message.guild
            user = message.author
            
            s = getServer(self, server.id)
            u = getUser(self, user.id)
            
            u.last_guild = server.id
            
            g_exp:float = s.server_exp_mult * random.uniform(u.level*0.8, u.level*1.2)
            g_money:float = s.server_money_mult * random.uniform(u.level*0.8, u.level*1.2)
            
            # 0.2~0.5 + rep
            gain = random.uniform(0.75, 1.25) + u.rep
            
            g_exp *= gain
            g_money *= gain
            
            u.wallet += g_money
            u.exp += g_exp
            
            self.db.update_value('users', 'data_user', user.id, u.save())
            self.db.update_value('servers', 'data_server', server.id, s.save())
            self.db.save()
            
        if self.user.mentioned_in(message):
            response = discord.Embed(
                title='Olá!',
                description='Eu sou o NineSix 🇧🇷, uma Applicação do Discord!',
                colour=discord.Color.purple()
            )
            await message.reply(embed=response)

client = Bot(intents=intents)
t = discord.app_commands.CommandTree(client=client)

@t.error
async def on_app_command_error(interaction: discord.Interaction, error: discord.app_commands.CommandInvokeError):
    if isinstance(error, discord.app_commands.CommandOnCooldown):
        # Humanize error.retry_after
        s, ms = divmod(error.retry_after, 1)
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        d, h = divmod(h, 24)
        
        
        await interaction.channel.send(f"Você precisa esperar {int(d)} dias, {int(h)} horas, {int(m)} minutos e {int(s)} segundos para usar esse comando novamente!")
    else:
        await interaction.channel.send(f"Erro: {error}")