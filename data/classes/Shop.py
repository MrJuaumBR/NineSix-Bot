from discord.ui import View, button, Button, Select
from discord import ButtonStyle, Interaction, Embed, SelectOption, Client
from .User import User as UserType
from typing import Literal
from ..globals import *

Items = ItemObj()

def more_exp_multiplier(server):
    server.server_exp_mult += 0.1
    
def give_item(item:str, amount:int,user_id:int, client:Client):
    user:UserType = client.getUser(user_id)
    if type(user._tools) != dict: # Fix old users
        user._tools = {}
        
    i:Item = Items.findByName(item)
    
    if str(item) in user.tools.keys():
        user._tools[str(i.id)]['amount'] += amount
        user._tools[str(i.id)]['usages'] += i.usages * amount
    else:
        user._tools[str(i.id)] = {
            'item_data': i.__dict__,
            'amount': amount,
            'usages': i.usages * amount
        }
    
    client.db.update_value('users', 'data_user', user_id, user.save())
    client.db.save()

class ServerShop:
    items: list[Product,] = []
    
    actual_page: int = 0
    
    def __init__(self):
        self.actual_page = 0
    
    def add_item(self, item):
        self.items.append(item)
    
    def get_items_page(self, page):
        return self.items[page * 5 : (page + 1) * 5]

class ServerShopView(View):
    def __init__(self, shop, user, client):
        super().__init__()
        self.shop = shop
        self.user = user
        self.client = client
        self.actual_page = 0
        self.selected = None
        self.items = self.shop.get_items_page(self.actual_page)
        self.select = Select(placeholder='Selecione um item para comprar', options=self.get_options(), min_values=1, max_values=1)
        self.select.callback = self.selectCallback
        self.add_item(self.select)
        
    async def selectCallback(self, interaction: Interaction):
        selected_in_page = int(self.select.values[0]) 
        self.selected = self.actual_page * 5 + selected_in_page
        await interaction.response.defer()
        
    def get_options(self):
        options = []
        for i, item in enumerate(self.items):
            options.append(SelectOption(label=item.name, value=str(i)))
        return options

    async def update_embed(self,interaction: Interaction):
        self.remove_item(self.select)
        self.items = self.shop.get_items_page(self.actual_page)
        new_select = Select(placeholder='Selecione um item para comprar', options=self.get_options(), min_values=1, max_values=1)
        new_select.callback = self.selectCallback
        self.add_item(new_select)
        self.select = new_select
            
        e = Embed(
            title='Servidor Shop',
            description=f'Itens a venda para o servidor:\n*Dinheiro do banco será utilizado para comprar itens*\n',
            color=0x00FF00
        )
        for i, item in enumerate(self.shop.get_items_page(self.actual_page)):
            e.add_field(name=f"{i+1}. {item.name}", value=f"{item.description} - ``S${self.client.humanize_cash(item.price)}``", inline=False)
            
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{(len(self.shop.items)//5) + 1}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        await interaction.response.edit_message(embed=e, view=self)
    
    @button(label='Anterior', style=ButtonStyle.green)
    async def back(self, interaction: Interaction, button: Button):
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = (len(self.shop.items)-1)//5
       
        await self.update_embed(interaction)
        
    @button(label='Proximo', style=ButtonStyle.green)
    async def next(self, interaction: Interaction, button: Button):
        self.actual_page += 1
        if self.actual_page >= (len(self.shop.items)+1)//5:
            self.actual_page = 0
        
        await self.update_embed(interaction)
        
    @button(label='Comprar', style=ButtonStyle.green)
    async def buy(self, interaction: Interaction, button: Button):
        if self.selected is not None:
            item = self.shop.items[self.selected]
            u = self.client.getUser(interaction.user.id)
            if u.bank >= item.price:
                u.bank -= item.price
                self.client.db.update_value('users', 'data_user', self.user.id, u.save())
                self.client.db.save()
                await interaction.response.send_message(f'Você comprou: {item.name}', ephemeral=True)
            else:
                await interaction.response.send_message('Dinheiro insuficiente.', ephemeral=True)
        else:
            await interaction.response.send_message('Selecione um item para comprar.', ephemeral=True)
            
    @button(label='Fechar', style=ButtonStyle.red)
    async def close(self, interaction: Interaction, button: Button):
        self.stop()
        self.clear_items()
        
        await interaction.response.edit_message(content='Shop fechado.', view=self, ephemeral=True)
class UserShop:
    items: list[Product,] = []
    
    actual_page: int = 0
    
    def __init__(self):
        self.actual_page = 0
    
    def add_item(self, item):
        self.items.append(item)
    
    def get_items_page(self, page):
        return self.items[page * 6 : (page + 1) * 6]
    
class UserShopView(View):
    def __init__(self, shop:UserShop, user, client:Client):
        super().__init__()
        self.shop = shop
        self.user = user
        self.client = client
        self.actual_page = 0
        self.selected = None
        self.quantity = 1
        self.items = self.shop.get_items_page(self.actual_page)
        self.select = Select(placeholder='Selecione um item para comprar', options=self.get_options(), min_values=1, max_values=1)
        self.select.callback = self.selectCallback
        self.quantity_select = Select(placeholder='Quant.', options=[SelectOption(label=f'{i}', value=f'{i}', default=(i == self.quantity)) for i in range(1,6,1)], min_values=1, max_values=1)
        self.quantity_select.callback = self.quantityCallback
        self.add_item(self.select)
        self.add_item(self.quantity_select)
        
    async def selectCallback(self, interaction: Interaction):
        selected_in_page = int(self.select.values[0]) 
        self.selected = self.actual_page * 6 + selected_in_page
        await interaction.response.defer()
        
    async def quantityCallback(self, interaction: Interaction):
        self.quantity = int(self.quantity_select.values[0])
        # Update default value of quantity_select
        self.remove_item(self.quantity_select)
        self.quantity_select = Select(placeholder='Quant.', options=[SelectOption(label=f'{i}', value=f'{i}', default=(i == self.quantity)) for i in range(1,6,1)], min_values=1, max_values=1)
        self.quantity_select.callback = self.quantityCallback
        self.add_item(self.quantity_select)
        await self.update_embed(interaction, 'next')
        
    def get_options(self):
        options = []
        for i, item in enumerate(self.items):
            options.append(SelectOption(label=item.name, value=str(i)))
        return options
    
    async def update_embed(self,interaction: Interaction, react_type:Literal['next', 'back']):
        self.remove_item(self.select)
        self.items = self.shop.get_items_page(self.actual_page)
        if self.items in [None,[]]:
            print('Something went wrong, Shop page is empty')
            if react_type == 'next':
                self.actual_page -= 1
            else:
                self.actual_page += 1
            await self.update_embed(interaction, react_type)
            return
        new_select = Select(placeholder='Selecione um item para comprar', options=self.get_options(), min_values=1, max_values=1)
        new_select.callback = self.selectCallback
        self.add_item(new_select)
        self.select = new_select
        e = Embed(
            title='User Shop',
            description=f'Itens a venda para o jogador:\n*Dinheiro do banco será utilizado para comprar itens*\n',
            color=0x00FF00
        )
        
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{(len(self.shop.items)+1)//6}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        self.create_fields(e, self.actual_page)
        await interaction.response.edit_message(embed=e, view=self)
    
    def create_fields(self, e:Embed, page:int):
        for i, item in enumerate(self.shop.get_items_page(page)):
            uItem = RawItems.findByName(item.name)
            e.add_field(name=f"{i+1}. {item.name}", value=f"{item.description} - ``por {self.quantity} = S${self.client.humanize_cash(item.price*self.quantity)}``, Nível: **{uItem.level}**", inline=False)
    
    @button(label='Anterior', style=ButtonStyle.green)
    async def back(self, interaction: Interaction, button: Button):
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = (len(self.shop.items)-1)//6
        
        await self.update_embed(interaction, 'back')
        
    @button(label='Proximo', style=ButtonStyle.green)
    async def next(self, interaction: Interaction, button: Button):
        self.actual_page += 1
        if self.actual_page >= (len(self.shop.items)+1)//6:
            self.actual_page = 0
            
        await self.update_embed(interaction , 'next') 
        
    @button(label='Comprar', style=ButtonStyle.green)
    async def buy(self, interaction: Interaction, button: Button):
        if self.selected is not None:
            item:Product = self.shop.items[self.selected]
            u = self.client.getUser(interaction.user.id)
            if u.bank >= item.price*self.quantity:
                u.bank -= item.price*self.quantity
                self.client.db.update_value('users', 'data_user', self.user.id, u.save())
                self.client.db.save()
                item.action(item=item.name,amount=self.quantity,user_id=interaction.user.id, client=self.client)
                await interaction.response.send_message(f'você comprou: {item.name}', ephemeral=True)
            else:
                await interaction.response.send_message('Dinheiro insuficiente.', ephemeral=True)
        else:
            await interaction.response.send_message('Selecione um item para comprar.', ephemeral=True)
            
    @button(label='Fechar', style=ButtonStyle.red)
    async def close(self, interaction: Interaction, button: Button):
        self.stop()
        self.clear_items()
        
        await interaction.response.edit_message(embed=Embed(description='Shop fechado.', color=0xFF0000), view=self)
    
    
Server_Items = [
    Product(name='Aumento de experiencia', price=10000, description='Aumenta o ganho de experiencia em 10%.', action=more_exp_multiplier),
    Product(name='Aumento de dinheiro', price=10000, description='Aumenta o ganho de dinheiro em 10%.', action=more_exp_multiplier),
    Product(name='Minerador Astuto', price=10000, description='Aumenta o dinheiro da mineração em 10%.', action=more_exp_multiplier),
    Product(name='Horas Extras', price=10000, description='Aumenta o dinheiro do trabalho em 10%.', action=more_exp_multiplier),
    Product(name='Aumento do diário', price=10000, description='Aumenta o dinheiro recebido do diário em 10%.', action=more_exp_multiplier),
    Product(name='Pesque e Receba', price=10000, description='Aumenta o dinheiro recebido da pesca em 10%.', action=more_exp_multiplier),
]

User_Items = [
    Product(name='Varinha de pesca(Madeira)', price=100, description='Habilita a pesca, 5 usos.', action=give_item),
    Product(name='Varinha de pesca(Cobre)', price=500, description='Habilita a pesca, 26 usos.', action=give_item),
    Product(name='Varinha de pesca(Prata)', price=2500, description='Habilita a pesca, 131 usos.', action=give_item),
    Product(name='Varinha de pesca(Ouro)', price=10000, description='Habilita a pesca, 656 usos.', action=give_item),
    Product(name='Varinha de pesca(Diamante)', price=50000, description='Habilita a pesca, 3281 usos.', action=give_item),
    Product(name='Varinha de pesca(Obsidiana)', price=1000000, description='Habilita a pesca, Inquebrável.', action=give_item),
    Product(name='Picareta(Madeira)', price=100, description='Habilita a mineração, 5 usos.', action=give_item),
    Product(name='Picareta(Cobre)', price=500, description='Habilita a mineração, 26 usos.', action=give_item),
    Product(name='Picareta(Prata)', price=2500, description='Habilita a mineração, 131 usos.', action=give_item),
    Product(name='Picareta(Ouro)', price=10000, description='Habilita a mineração, 656 usos.', action=give_item),
    Product(name='Picareta(Diamante)', price=50000, description='Habilita a mineração, 3281 usos.', action=give_item),
    Product(name='Picareta(Obsidiana)', price=1000000, description='Habilita a mineração, Inquebrável.', action=give_item),
    Product(name='Machado(Madeira)', price=100, description='Habilita o corte de madeira, 5 usos.', action=give_item),
    Product(name='Machado(Cobre)', price=500, description='Habilita o corte de madeira, 26 usos.', action=give_item),
    Product(name='Machado(Prata)', price=2500, description='Habilita o corte de madeira, 131 usos.', action=give_item),
    Product(name='Machado(Ouro)', price=10000, description='Habilita o corte de madeira, 656 usos.', action=give_item),
    Product(name='Machado(Diamante)', price=50000, description='Habilita o corte de madeira, 3281 usos.', action=give_item),
    Product(name='Machado(Obsidiana)', price=1000000, description='Habilita o corte de madeira, Inquebrável.', action=give_item),
]