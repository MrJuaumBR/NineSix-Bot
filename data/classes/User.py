import pickle, asyncio, datetime
from discord import Guild, TextChannel, utils
from JPyDB import Database
from .Server import Server

from ..globals import *

save_keys = ['_premium', '_level', '_exp', '_wallet', '_bank', '_tools', '_rep', '_equipped_equipment', '_items', '_combat_data']

default_combat_data = {
    'attacks': [],
    'life':100,
    'max-life':100,
    'mana':100,
    'max-mana':100,
    'armor':0,
    'max-armor':0,
    'equipped-attacks':[],
    'last-attack-received':None,
}

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
        'accessory-1':None,
        'accessory-2':None
    }
    last_guild: Guild = None
    _combat_data: dict = {}
    
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
        if self._exp >= 100*self._level: # Level up
            # Needs to known hoy many levels will up
            levels_up = self._exp // (100*self._level)
            self._exp -= (100*self._level) * levels_up
            self.level += levels_up
            if self.last_guild != None:
                s = Server(0).load(self.client.db.findByText('servers', 'id', self.last_guild)['data_server'])
                if s.level_up_channel != None:
                    channel:TextChannel = self.client.get_channel(s.level_up_channel)
                    async def _send_message():
                        await channel.send(f'**<@{self.id}>** alcançou o nível **{int(self.level)}**! (+{int(levels_up)}) 🎉')
                    self.client.loop.create_task(_send_message())
                self.client.db.update_value('users', 'data_user', self.id, self.save())
                self.client.db.save()
        elif self._exp < 0: # Level down
            self.level -= 1
            self._exp = (100*self._level) - abs(self._exp)
    
                
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
            'combat_data': default_combat_data
        }
        self.last_guild = None
        self.data_user.setdefault('combat_data', default_combat_data)
        self.__dict__.setdefault('_combat_data', default_combat_data)
        
        
        self.load_data_user()
        
    def heal_sys(self):    
        a, m = self.get_life_info()
        if a < m:
            if self._combat_data['last-attack-received'] == None:
                self._combat_data['life'] = m
            else:
                elapsed = (datetime.datetime.now() - self._combat_data['last-attack-received']).total_seconds()
                if elapsed >= 5:
                    intervals = int(elapsed//5)
                    heal_amount = (0.1 * m)* intervals
                    # Recover 10% of life per 5 seconds, need to use datetime to calculate because of bot restart
                    self._combat_data['life'] = min(a + heal_amount, m)
                    self.client.db.update_value('users', 'data_user', self.id, self.save())
                    self.client.db.save()
                
    
    def getToolById(self, item_id:int) -> dict:
        return self.tools[item_id] if item_id in self.tools.keys() else None    
    def getItemById_(self, item_id:str) -> dict:
        return self.items[item_id] if item_id in self.items.keys() else None
    
    def getItemById(self, item_id:str) -> dict:
        x = self.getToolById(item_id)
        if x == None:
            x = self.getItemById_(item_id)
        return x
    
    def takeDamage(self, damage:int) -> bool:
        self._combat_data['life'] -= damage
        if self._combat_data['life'] < 0: self._combat_data['life'] = 0
        
        self._combat_data['last-attack-received'] = datetime.datetime.now()
        return True
            
    
    def equipAbility(self, ability_id:str):
        if ability_id in self._combat_data['equipped-attacks']:
            self._combat_data['equipped-attacks'].remove(ability_id)
        elif ability_id in self._combat_data['attacks']:
            if len(self._combat_data['equipped-attacks']) >= 5: return
            self._combat_data['equipped-attacks'].append(ability_id)
    
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
            return dataIsFrom[item_id]
        elif item_id in self.tools.keys():
            dataIsFrom:dict = self.tools
            return dataIsFrom[item_id]
        else:
            return None
    
    def getItems(self, category:ItemsTypes=None, subtype:str=None, exclude:list[str,]=[]) -> list:
        c = []
        if category is not None:
            for item in self.items.values():
                if item['item_data']['item_type'] == category:
                    c.append(item)
            for tool in self.tools.values():
                if tool['item_data']['item_type'] == category:
                    c.append(tool)
        elif subtype is not None:
            for item in self.items.values():
                if item['item_data']['subtype'] == subtype:
                    c.append(item)
            for tool in self.tools.values():
                if tool['item_data']['subtype'] == subtype:
                    c.append(tool)
        else:
            for item in self.items.values():
                if item['item_data']['id'] not in exclude:
                    c.append(item)
            for tool in self.tools.values():
                if tool['item_data']['id'] not in exclude:
                    c.append(tool)
        return c
    
    def getTotalItems(self, category:ItemsTypes=None, subtype:str=None) -> int:
        return len(self.getItems(category, subtype))
    
    def getTotalSkills(self) -> int:
        return len(self._combat_data['attacks'])
    
    def deleteTool(self, category:ItemsTypes):
        toolId = self._equipped_equipment[category]
        if toolId != None:
            del self._tools[toolId]
            self._equipped_equipment[category] = None
    
    def getEquipped(self, item_type:ItemsTypes) -> dict: 
        if item_type == 'ability': return self.get_equipped_attacks()
        elif self.equipped_equipment[item_type] == None:
            return None
        return self.getItemById(self.equipped_equipment[item_type])
    
    def equip(self, item_type:ItemsTypes, item_id:str):
        t = self.getItemById(item_id)
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
    
    def get_life_info(self) -> tuple[float, float]:
        return self._combat_data['life'], self._combat_data['max-life']
    
    def get_life_percentage(self) -> float:
        return self._combat_data['life'] / self._combat_data['max-life']
    
    def get_mana_info(self) -> tuple[float, float]:
        return self._combat_data['mana'], self._combat_data['max-mana']
    
    def get_mana_percentage(self) -> float:
        return self._combat_data['mana'] / self._combat_data['max-mana']
    
    def add_attack(self, attack_id:str):
        attack = CHandler.get_attack_by_id(attack_id)
        if attack and attack not in self._combat_data['attacks']:
            self._combat_data['attacks'].append(attack)
            
    def get_attacks(self):
        return self._combat_data['attacks']
    
    def get_equipped_attacks(self) -> list[str, ]:
        return self._combat_data['equipped-attacks']
        
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
            
    def remove_item(self, item_id:int, amount:int = 1):
        if str(item_id) in self.items.keys():
            self.items[str(item_id)]['amount'] -= amount
            if self.items[str(item_id)]['amount'] <= 0:
                del self.items[str(item_id)]
    
    def load_data_user(self):
        for key in self.data_user.keys():
            self.__setattr__(f'_{key}', self.data_user[key])    
            
        # Run Life Sys
        self.heal_sys()
    
    def load(self, data: bytes):
        d:dict = {}
        d = dict(pickle.loads(data))
        
        for key in d.keys():
            if key == '_combat_data':
                self.data_user[key] = self.combat_data_format(d[key], 'load')
            else:
                self.data_user[key] = d[key]                
                
        self.load_data_user()
        
        
        return self
    def combat_data_format(self, data, process:Literal['save','load']='save') -> dict:
        if process == 'save':
            r = {}
            for key in data.keys():
                value = data[key]
                if key in ['attacks', 'equipped-attacks']:
                  if not key in r.keys():
                    r[key] = []
                  for attack in value: r[key].append(attack.id if isinstance(attack, Attack) else attack)
                else:
                  r[key] = value
            return r  
        elif process == 'load':
            r = {}
            for key in data.keys():
                value = data[key]
                if key in ['attacks', 'equipped-attacks']:
                  if not key in r.keys():
                    r[key] = []
                  for attack in value: r[key].append(CHandler.get_attack_by_id(attack))
                else:
                  r[key] = value
            return r
    
    def save(self) -> bytes:
        d = {}
        for key in save_keys:
            if key in self.__dict__.keys():
                if key == '_combat_data':
                    d[(key if not key.startswith('_') else key[1:])] = self.combat_data_format(self.__dict__[key], 'save')
                else:
                    d[(key if not key.startswith('_') else key[1:])] = self.__dict__[key]
        return pickle.dumps(d)

class UserShop:
    def __init__(self, user_id:int) -> None:
        self.id = user_id
        self.items:list[dict,] = []
        