from typing import Literal
import random
attack_types = Literal['physical', 'magic', 'slash', 'knockback', 'weapon']

class Attack:
    CombatHandler:object
    id:str
    name:str
    damage:int
    type_of_damage:str
    level:int
    mana_cost:int
    description:str
    def __init__(self, CombatHandler, id:str, name:str, damage:int, type_of_damage:attack_types, level:int, mana_cost:int, description:str):
        self.CombatHandler = CombatHandler
        self.id = id
        self.name = name
        self.damage = damage
        self.type_of_damage = type_of_damage
        self.level = level
        self.mana_cost = mana_cost
        self.description = description


class Enemy:
    CombatHandler:object
    id:str
    name:str
    level:int
    maxlife:float
    life:float
    drops:dict = {}
    rewards:tuple[float, float] # (gold, exp)
    attacks:list[Attack,]
    damage_sum:int
    def __init__(self, CombatHandler, id:str, name:str, level:int, maxlife:float, drops:list[str, ], rewards:tuple[float, float], attacks:list[str,], damage_sum:int=0):
        self.CombatHandler = CombatHandler
        self.id = id
        self.name = name
        self.level = level
        self.maxlife = maxlife
        self.life = maxlife
        self.drops = drops
        self.rewards = rewards
        self.attacks = [CombatHandler.get_attack_by_id(attack_id) if type(attack_id) == str else attack_id for attack_id in attacks]
        self.damage_sum = damage_sum

    def takeDamage(self, damage:int):
        self.life -= damage
        if self.life < 0: self.life = 0

    def get_life_info(self) -> tuple[float, float]:
        return self.life, self.maxlife
    
    def get_life_percentage(self) -> float:
        return self.life / self.maxlife
    
    def get_random_reward(self, luck:float=1.0) -> list:
        # Luck random reward
        a = []
        for drop in self.drops:
            y = luck * random.random()
            if y >=  drop['chance']:
                a.append(drop['id'])
                y -= drop['chance']
        return a
        
    def get_random_attack(self) -> tuple[Attack, int]:
        return random.choice(self.attacks), self.damage_sum
        
class CombatHandler:
    attacks:list[Attack,] = []
    enemies:list[Enemy,] = []
    def __init__(self):
        self.attacks:list[Attack,] = [
            Attack(self,'attack_punch', 'Soco', 10,'physical', 1, 0, 'Apenas um soco normal'),
            Attack(self, 'attack_kick', 'Chute', 15, 'physical', 1, 0, 'Um chute normal'),
            Attack(self, 'attack_assault', 'Investida', 25, 'physical', 1, 0, 'Um empurrão forte'),
            Attack(self, 'attack_rest', 'Descansar', 0, 'magic', 1, 70, 'Recupera 1% ~ 4% da vida máxima'),
            Attack(self, 'attack_impact', 'Impacto', 40, 'physical', 5, 20, 'Um ataque forte que causa um grande impacto'),
            Attack(self, 'attack_magic_missile', 'Míssil Mágico', 30, 'magic', 10, 30, 'Um ataque mágico que causa dano moderado'),
        ]
        self.enemies_args:list[tuple,] = [
            (self,'goblin_basic', 'Goblin', 1, 50, [{'id':'bone', 'chance':0.5}, {'id':'cloth', 'chance':0.3}, {'id':'leather', 'chance':0.2}], (10,10), ['attack_punch','attack_kick']),
            (self,'goblin_giant', 'Goblin Gigante', 5, 100, [{'id':'bone', 'chance':0.3}, {'id':'cloth', 'chance':0.4}, {'id':'leather', 'chance':0.3}], (20,10), ['attack_punch','attack_kick']),
            (self,'skeleton_basic', 'Skeleton', 5, 70, [{'id':'bone', 'chance':1.0}], (10,10), ['attack_punch','attack_assault']),
            (self,'goblin_sorcerer', 'Goblin Feiticeiro', 10, 70, [{'id':'bone', 'chance':0.2}, {'id':'cloth', 'chance':0.5}, {'id':'leather', 'chance':0.3}], (30,20), ['attack_impact','attack_magic_missile','attack_rest'], 10),
        ]
        self.enemies:list[Enemy,] = [Enemy(*args) for args in self.enemies_args]
    
    def getEnemys(self, level:int=None, exclude:list[str,]=[], level_range:tuple[int,int]=None) -> list[Enemy]:
        x = []
        for enemy in self.enemies:
            if level_range is not None:
                if enemy.level >= level_range[0] and enemy.level <= level_range[1]:
                    if not (enemy.id in exclude): x.append(enemy)
            elif level is not None:
                if enemy.level <= level:
                    if not (enemy.id in exclude): x.append(enemy)
            else:
                if enemy.id in exclude: pass
                else: x.append(enemy)
                
        return x
    
    def getRandomEnemy(self, level:int=None, exclude:list[str,]=[], level_range:tuple[int,int]=None) -> Enemy:
        return random.choice(self.getEnemys(level, exclude, level_range))
    
    def getRandomEnemyNew(self, level:int=None, exclude:list[str,]=[], level_range:tuple[int,int]=None) -> Enemy:
        x = random.choice(self.getEnemys(level, exclude, level_range))
        return Enemy(self, x.id, x.name, x.level, x.maxlife, x.drops, x.rewards, x.attacks, x.damage_sum)
    
    def get_attack_by_id(self, attack_id:str) -> Attack:
        for attack in self.attacks:
            if attack.id == attack_id:
                return attack
            
        return None