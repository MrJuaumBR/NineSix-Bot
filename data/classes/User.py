import pickle, asyncio
from discord import Guild, TextChannel, utils
from JPyDB import Database
from .Server import Server

from ..globals import *

save_keys = ['_premium', '_level', '_exp', '_wallet', '_bank', '_tools', '_rep', '_equipped_equipment', '_items']

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
    _items: dict = {}
    _tools: dict = {}
    _rep: int = 0
    _equipped_equipment: dict = {
        'axe':None,
        'pickaxe':None,
        'fishing_rod':None,
        'weapon':None,
    }
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
    def items(self): return self._items
    @property
    def tools(self) -> dict:
        # If tools is not a dict, return an empty dict
        if type(self._tools) != dict:
            return {}
        return self._tools
    @property
    def rep(self): return self._rep
    @property
    def equipped_equipment(self): return self._equipped_equipment
        
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
    @items.setter
    def items(self, value): self._items = value
    @tools.setter
    def tools(self, value): self._tools = value
    @rep.setter
    def rep(self, value): self._rep = value
    @equipped_equipment.setter
    def equipped_equipment(self, value): self._equipped_equipment = value
        
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
            'items': {},
            'rep': 0,
            'equipped_equipment': {
                'axe':None,
                'pickaxe':None,
                'fishing_rod':None,
                'weapon':None,
            },
        }
        self.last_guild = None
        
        self.load_data_user()
        
    def getToolById(self, item_id:int) -> dict:
        return self.tools[item_id] if item_id in self.tools.keys() else None    
    def getItemById_(self, item_id:str) -> dict:
        return self.items[item_id] if item_id in self.items.keys() else None
    
    def getItemById(self, item_id:str) -> dict:
        x = self.getToolById(item_id)
        if x == None:
            x = self.getItemById_(item_id)
        return x
    
    def getToolsByType(self, category:ItemsTypes) -> list:
        x = []
        for raw_tool in self.tools.values():
            tool_data = raw_tool['item_data']
            if 'item_type' in tool_data and tool_data['item_type'] == category:
                x.append(raw_tool)
        return x
    
    def findItem(self, item_id:int) -> dict:
        if item_id in self.items.keys():
            dataIsFrom:dict = self.items
        else:
            dataIsFrom:dict = self.tools
        return dataIsFrom[item_id]
    
    def getTotalItems(self) -> int:
        return len(self.items) + len(self.tools)
    
    def deleteTool(self, category:ItemsTypes):
        toolId = self._equipped_equipment[category]
        if toolId != None:
            del self._tools[toolId]
            self._equipped_equipment[category] = None
    
    def getEquipped(self, item_type:ItemsTypes) -> dict: 
        if self.equipped_equipment[item_type] == None:
            return None
        return self.getToolById(self.equipped_equipment[item_type])
    
    def equip(self, item_type:ItemsTypes, item_id:str):
        t = self.getToolById(item_id)
        if t:
            # Check if i can stay using it(It haves any usages left? or it is unbreakable?)
            if t['item_data']['unbreakable'] or t['usages'] > 0:
                self._equipped_equipment[item_type] = item_id
            else:
                print('Why are you trying to equip something that is broken?')
        else:
            print('Why are you trying to equip something that you don\'t have?')
                
    def unequip(self, item_type:ItemsTypes):
        self._equipped_equipment[item_type] = None
    
    def add_item(self, item_id:int, amount:int = 1):
        i:Item = RawItems.findById(item_id)
        if str(item_id) in self.items.keys():
            self.items[str(item_id)]['amount'] += amount
            if not i.item_type in ['fish', 'material']:
                self.items[str(item_id)]['usages'] += i.usages * amount
        else:
            self.items[str(item_id)] = {
                'item_data': i.__dict__,
                'amount': amount,
                'usages': i.usages * amount
            }
            
            
    
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