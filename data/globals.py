from typing import Literal
import math, json

ItemsTypes = Literal['weapon', 'fishing_rod', 'pickaxe', 'axe', 'woods', 'material','fish']
BotData = json.load(open('data/data.json', 'rb'))
BotEmojis = BotData['emojis']
BotCrafts = BotData['crafts']

def GetEmoji(id:str) -> str:
    if f'ns_{id}' in BotEmojis.keys(): return BotEmojis[f'ns_{id}']
    else: return ''

class Product:
    name: str
    price: int
    description: str
    action: object
    
    def __init__(self, name, price, description, action):
        self.name = name
        self.price = price
        self.description = description
        self.action = action
    
    def buy(self, **kwargs):
        self.action(**kwargs)
            
class Item:
    id:str
    name:str
    usages:int
    level:int
    item_type:ItemsTypes = None
    unbreakable:bool = False
    subtype:str = None
    findable:bool = False
    description:str = ''
    def __init__(self, id:str, name:str, usages:int, level:int, item_type:ItemsTypes, unbreakable:bool=False, subtype:str=None, findable:bool=False, description:str=''):
        self.id = id
        self.name = name
        self.usages = usages
        self.level = level
        self.unbreakable = unbreakable
        self.item_type = item_type
        self.subtype = str(subtype).lower()
        self.findable = findable
        self.description = description
        
        self.emoji = f'ns_{self.id}'

class ItemObj:
    values:list[Item,] = [
        Item('fishing_rod_wood', 'Varinha de pesca(Madeira)', 3, 1, 'fishing_rod', description='Uma varinha de pesca para inciantes.'), # Varinha de pesca
        Item('fishing_rod_copper', 'Varinha de pesca(Cobre)', 15, 1, 'fishing_rod', description='Uma varinha de pesca para iniciantes. *Um pouco melhores...*'),
        Item('fishing_rod_silver', 'Varinha de pesca(Prata)', 45, 5, 'fishing_rod', description='Uma varinha de pesca para amadores.'),
        Item('fishing_rod_gold', 'Varinha de pesca(Ouro)', 200, 10, 'fishing_rod', description='Uma varinha de pesca para profissionais.'),
        Item('fishing_rod_diamond', 'Varinha de pesca(Diamante)', 500, 15, 'fishing_rod', description='Uma varinha de pesca para mestres.'),
        Item('fishing_rod_obsidian', 'Varinha de pesca(Obsidiana)', 1, 20, 'fishing_rod', True, description='Uma varinha de pesca para mestres absolutos.'),
        Item('pickaxe_wood', 'Picareta(Madeira)', 3, 1, 'pickaxe'), # Picareta
        Item('pickaxe_copper', 'Picareta(Cobre)', 15, 1, 'pickaxe'),
        Item('pickaxe_silver', 'Picareta(Prata)', 45, 5, 'pickaxe'),
        Item('pickaxe_gold', 'Picareta(Ouro)', 200, 10, 'pickaxe'),
        Item('pickaxe_diamond', 'Picareta(Diamante)', 500, 15, 'pickaxe'),
        Item('pickaxe_obsidian', 'Picareta(Obsidiana)', 1, 20, 'pickaxe', True),
        Item('axe_wood', 'Machado(Madeira)', 3, 1, 'axe'), # Machado
        Item('axe_copper', 'Machado(Cobre)', 15, 1, 'axe'),
        Item('axe_silver', 'Machado(Prata)', 45, 5, 'axe'),
        Item('axe_gold', 'Machado(Ouro)', 200, 10, 'axe'),
        Item('axe_diamond', 'Machado(Diamante)', 500, 15, 'axe'),
        Item('axe_obsidian', 'Machado(Obsidiana)', 1, 20, 'axe', True),
        # Weapons
        Item('weapon_club', 'Porrete', 3, 1, 'weapon', subtype='club'),
        Item('weapon_copper_knife', 'Faca de Cobre', 5, 1, 'weapon', subtype='knife'),
        Item('weapon_silver_knife', 'Faca de Prata', 7, 1, 'weapon', subtype='knife'),
        Item('weapon_club_spiked', 'Porrete com Espinhos', 15, 10, 'weapon', subtype='club'),
        # Woods
        Item('wood_oak', 'Madeira de carvalho', 1, 1, 'woods'),
        # Fishes
        Item('fish_small', 'Peixe Pequeno', 1, 1, 'fish'),
        Item('fish_jade', 'Peixe Chifre-de-Jade', 1, 1, 'fish'),
        Item('fish_marfim', 'Peixe Chifre-de-Marfim', 1, 1, 'fish'),
        Item('fish_coral', 'Peixe Chifre-de-Coral', 1, 1, 'fish'),
        Item('fish_tiger', 'Enguias de tigre', 1, 1, 'fish'),
        Item('fish_platinum', 'Peixe prata', 1, 1, 'fish'),
        Item('fish_blue', 'Peixe azul', 1, 1, 'fish'),
        Item('fish_red', 'Peixe vermelho', 1, 1, 'fish'),
        Item('fish_silver', 'Peixe Prata', 1, 1, 'fish'),
        # Materials
        Item('wood_stick','Graveto', 0, 1, 'material', True, 'stick', True),
        Item('rock_stone','Pedra', 0, 1, 'material', True, 'rock', True),
        Item('plant_grass','Grama', 0, 1, 'material', True, 'plant', True),
        Item('plant_herbs','Ervas', 0, 1, 'material', True, 'plant', True),
        Item('bone','Osso', 0, 1, 'material', True, 'bone', True),
        Item('iron_spikes','Espinhos de Ferro', 0, 10, 'material', True),
        # Ores
        Item('ore_tin','Minério de Estanho', 0, 1, 'material', True, 'ore', False),
        Item('ore_copper','Minério de Cobre', 0, 1, 'material', True, 'ore', False),
        Item('ore_silver','Minério de Prata', 0, 1, 'material', True, 'ore', False),
        Item('ore_iron','Minério de Ferro', 0, 10, 'material', True, 'ore', False),
        Item('ore_brass','Minério de Latão', 0, 10, 'material', True, 'ore', False),
        Item('ore_gold','Minério de Ouro', 0, 10, 'material', True, 'ore', False),
        Item('ore_diamond','Minério de Diamante', 0, 15, 'material', True, 'ore', False),
        Item('ore_obsidian','Minério de Obsidiana', 0, 20, 'material', True, 'ore', False),
        Item('ore_manasteel','Minério de Manasteel', 0, 25, 'material', True, 'ore', False),
        # Bars
        Item('bar_tin','Barra de Estanho', 0, 1, 'material', True, 'bar', False),
        Item('bar_copper','Barra de Cobre', 0, 1, 'material', True, 'bar', False),
        Item('bar_silver','Barra de Prata', 0, 1, 'material', True, 'bar', False),
        Item('bar_iron','Barra de Ferro', 0, 10, 'material', True, 'bar', False),
        Item('bar_brass','Barra de Latão', 0, 10, 'material', True, 'bar', False),
        Item('bar_gold','Barra de Ouro', 0, 10, 'material', True, 'bar', False),
        Item('bar_diamond','Barra de Diamante', 0, 15, 'material', True, 'bar', False),
        Item(id='bar_obsidian',name='Barra de Obsidiana', usages=0, level=20, item_type='material', unbreakable=True, subtype='bar', findable=False),
        Item('bar_manasteel','Barra de Manasteel', 0, 25, 'material', True, 'bar', False),
    ]
    
    def getOreBar(self, item_id:str) -> str:
        for key, item in BotCrafts.items():
            if len(item['items']) <= 1:
                if item['items'][0]['id'] == item_id:
                    return key
    
    def canCraft(self, user, item_id:str) -> bool:
        if item_id in BotCrafts.keys():
            can_craft:bool = True
            for item in BotCrafts[item_id]['items']:
                require_item_id, item_amount = item['id'], item['amount']
                item_user = user.findItem(require_item_id)
                if item_user is None or item_user['amount'] < item_amount: can_craft = False
            if user.level < BotCrafts[item_id]['level']: can_craft = False
            return can_craft
        else: return False
        
    def getAll(self, category:ItemsTypes=None) -> list[Item,]:
        if category is not None: return [item for item in self.values if item.item_type == category]
        return self.values
    
    def order_by_usages(self, order:Literal['asc','desc'],data_list:list[Item,]=None) -> list[Item]:
        if data_list is None: data_list = self.values
        # Needs to sort by usages and if unbreakable
        if order == 'asc':
            return sorted(data_list, key=lambda x: (x.usages, x.unbreakable))
        else:
            return sorted(data_list, key=lambda x: (x.usages, x.unbreakable), reverse=True)
    def getCategory(self, category:ItemsTypes, level_limit:int=None) -> list[Item]:
        if level_limit is not None: return [item for item in self.values if item.item_type == category and item.level <= level_limit]
        else: return [item for item in self.values if item.item_type == category]
    
    def getSubtype(self, subtype:str, level_limit:int=None, exclude:list[str,]=[], level_range:tuple[int,int]=None) -> list[Item]:
        x = []
        for item in self.values:
            if str(item.subtype).lower() == str(subtype).lower():
                if level_range is not None:
                    if item.level >= level_range[0] and item.level <= level_range[1]:
                        if not (item.id in exclude): x.append(item)
                elif level_limit is not None:
                    if item.level <= level_limit:
                        if not (item.id in exclude): x.append(item)
                else:
                    if item.id in exclude: pass
                    else: x.append(item)
                    
        return x
    
    def getFindable(self) -> list[Item]:
        return [item for item in self.values if item.findable]
    
    def findByType(self, item_type:ItemsTypes) -> list[Item]:
        return [item for item in self.values if item.item_type == item_type]
    
    def findById(self,id:str) -> Item:
        for item in self.values:
            if item.id == id:
                return item
            
        return None
    
    def findByName(self,name:str) -> Item:
        for item in self.values:
            if item.name == name:
                return item
            
        return None
    
RawItems = ItemObj()
AllItemsIds = [str(i.id) for i in RawItems.values]