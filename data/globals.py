from typing import Literal
import math, json

ItemsTypes = Literal['weapon', 'fishing_rod', 'pickaxe', 'axe', 'woods', 'material','fish']
BotEmojis = json.load(open('data/emojis.json', 'rb'))

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
        Item('wood_oak', 'Madeira de carvalho', 1, 1, 'woods'), # Woods
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
        # Ores
        Item('ore_tin','Minério de Estanho', 0, 1, 'material', True, 'ore', True),
        Item('ore_copper','Minério de Cobre', 0, 1, 'material', True, 'ore', True),
        Item('ore_silver','Minério de Prata', 0, 1, 'material', True, 'ore', True),
        Item('ore_iron','Minério de Ferro', 0, 10, 'material', True, 'ore', True),
        Item('ore_brass','Minério de Latão', 0, 10, 'material', True, 'ore', True),
        Item('ore_gold','Minério de Ouro', 0, 10, 'material', True, 'ore', True),
        Item('ore_diamond','Minério de Diamante', 0, 15, 'material', True, 'ore', True),
        Item('ore_obsidian','Minério de Obsidiana', 0, 20, 'material', True, 'ore', True),
        Item('ore_manasteel','Minério de Manasteel', 0, 25, 'material', True, 'ore', True),
        # Bars
        Item('bar_tin','Barra de Estanho', 0, 1, 'material', True, 'bar', True),
        Item('bar_copper','Barra de Cobre', 0, 1, 'material', True, 'bar', True),
        Item('bar_silver','Barra de Prata', 0, 1, 'material', True, 'bar', True),
        Item('bar_iron','Barra de Ferro', 0, 10, 'material', True, 'bar', True),
        Item('bar_brass','Barra de Latão', 0, 10, 'material', True, 'bar', True),
        Item('bar_gold','Barra de Ouro', 0, 10, 'material', True, 'bar', True),
        Item('bar_diamond','Barra de Diamante', 0, 15, 'material', True, 'bar', True),
        Item('bar_obsidian','Barra de Obsidiana', 0, 20, 'material', True, 'bar', True),
        Item('bar_manasteel','Barra de Manasteel', 0, 25, 'material', True, 'bar', True),
    ]
    
    crafting = {
        'ore_tin': 'bar_tin',
        'ore_copper': 'bar_copper',
        'ore_silver': 'bar_silver',
        'ore_iron': 'bar_iron',
        'ore_brass': 'bar_brass',
        'ore_gold': 'bar_gold',
        'ore_diamond': 'bar_diamond',
        'ore_obsidian': 'bar_obsidian',
        'ore_manasteel': 'bar_manasteel',
    }
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
    
    def getSubtype(self, subtype:str, level_limit:int=None, exclude:list[str,]=None) -> list[Item]:
        if exclude is not None: return [item for item in self.values if item.subtype == str(subtype).lower() and item.name not in exclude]
        elif level_limit is not None: return [item for item in self.values if item.subtype == str(subtype).lower() and item.level <= level_limit]
        else: return [item for item in self.values if item.subtype == str(subtype).lower()]
    
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