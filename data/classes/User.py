import pickle, asyncio
from discord import Guild, TextChannel, utils
from JPyDB import Database
from .Server import Server

save_keys = ['_premium', '_level', '_exp', '_wallet', '_bank', '_tools', '_rep']

class User:
    id: int
    client:object
    db:Database
    data_user: dict
    
    _premium: bool = False
    _level: int = 1
    _exp: int = 0
    _wallet: int = 0
    _bank: int = 0
    _tools: dict = {}
    _rep: int = 0
    last_guild: Guild = None
    
    @property
    def premium(self): return self._premium
    @property
    def level(self): return self._level
    @property
    def exp(self): return self._exp
    @property
    def wallet(self): return self._wallet
    @property
    def bank(self): return self._bank
    @property
    def tools(self) -> dict:
        # If tools is not a dict, return an empty dict
        if type(self._tools) != dict:
            return {}
        return self._tools
    @property
    def rep(self): return self._rep
        
    @premium.setter
    def premium(self, value): self._premium = value
    @level.setter
    def level(self, value): self._level = value
    @exp.setter
    def exp(self, value):
        self._exp = round(value,2)
        if self._exp >= 100*self._level:
            self._exp -= 100*self._level
            self.level += 1
            if self.last_guild != None:
                s = Server(0).load(self.client.db.findByText('servers', 'id', self.last_guild)['data_server'])
                if s.level_up_channel != None:
                    channel:TextChannel = self.client.get_channel(s.level_up_channel)
                    async def _send_message():
                        await channel.send(f'**<@{self.id}>** alcançou o nível **{self.level}**!')
                    self.client.loop.create_task(_send_message())
                self.client.db.update_value('users', 'data_user', self.id, self.save())
                self.client.db.save()
    
                
    @wallet.setter
    def wallet(self, value): self._wallet = round(value,2)
    @bank.setter
    def bank(self, value): self._bank = round(value,2)
    @tools.setter
    def tools(self, value): self._tools = value
    @rep.setter
    def rep(self, value): self._rep = value
        
    def __init__(self, id:int, client:object):
        self.client = client
        self.id = id
        self.db = self.client.db
        self.data_user = {
            'premium': False,
            'level': 1,
            'exp': 0,
            'wallet': 0,
            'bank': 0,
            'tools': {},
            'rep': 0
        }
        self.last_guild = None
        
        self.load_data_user()
    
    def load_data_user(self):
        for key in self.data_user.keys():
            self.__setattr__(f'_{key}', self.data_user[key])    
    
    def load(self, data: bytes):
        d:dict = {}
        d = dict(pickle.loads(data))
        
        for key in d.keys():
            self.data_user[key] = d[key]                
                
        self.load_data_user()
        
        
        return self
    def save(self) -> bytes:
        d = {}
        for key in save_keys:
            if key in self.__dict__.keys():
                d[(key if not key.startswith('_') else key[1:])] = self.__dict__[key]
        return pickle.dumps(d)