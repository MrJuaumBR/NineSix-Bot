import discord
from discord import ui as dui
from .User import User as UserType
from .Shop import ItemObj, Item
from typing import Literal

class GiveItemView(dui.View):
    def __init__(self, user:UserType, user2:UserType, user2_client:discord.User, client:discord.Client):
        super().__init__()
        self.user = user
        self.user2_client = user2_client
        self.user2 = user2
        self.client = client
        
        self.actual_page = 0
        self.items_per_page = 8
        self.items = ItemObj()
        
        # 2 Select Ui, Quantity and Item
        self.UiItemSelected = dui.Select(placeholder='Selecione um item', options=self.get_options(), min_values=1, max_values=1)
        self.UiItemSelected.callback = self.UiItemSelectedCallback
        self.selected = None
        
        self.quantity = 1
        self.UiItemQuantity = dui.Select(placeholder='Quant.', options=[discord.SelectOption(label=f'{i}', value=f'{i}', default=(i == self.quantity)) for i in range(1,6,1)], min_values=1, max_values=1)
        self.UiItemQuantity.callback = self.UiItemQuantityCallback
        
        
        self.add_item(self.UiItemSelected)
        self.add_item(self.UiItemQuantity)
        
    async def UiItemSelectedCallback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.selected = int(self.UiItemSelected.values[0])
        await interaction.response.defer()
        
    async def UiItemQuantityCallback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.quantity = int(self.UiItemQuantity.values[0])
        await interaction.response.defer()
        
    async def update_embed(self, interaction: discord.Interaction, react_type:Literal['next', 'back'] = 'next'): 
        self.remove_item(self.UiItemSelected)
        self.remove_item(self.UiItemQuantity)
        self.UiItemQuantity = dui.Select(placeholder='Quant.', options=[discord.SelectOption(label=f'{i}', value=f'{i}', default=(i == self.quantity)) for i in range(1,6,1)], min_values=1, max_values=1)
        self.UiItemQuantity.callback = self.UiItemQuantityCallback
        self.add_item(self.UiItemQuantity)
        self.UiItemSelected = dui.Select(placeholder='Selecione um item', options=self.get_options(), min_values=1, max_values=1)
        self.UiItemSelected.callback = self.UiItemSelectedCallback
        self.add_item(self.UiItemSelected)
        
        e = discord.Embed(
            title='Itens disponíveis no seu inventário',
            color=0x00FF00
        )
        
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{(len(self.user.tools.keys())//self.items_per_page) + 1}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        
        items = self.get_items_page(self.actual_page)
        
        for i, item in enumerate(items):
            e.add_field(name=f"{i+1}. {item[0].name}", value=f"x``{item[1]}``", inline=False)
        
        await interaction.response.edit_message(embed=e, view=self)
        
    def get_items_page(self, page:int) -> list[tuple[Item, int]]:
        x = []
        for item_id in self.user.tools.keys():
            l:Item = self.items.findById(item_id)
            x.append((l, self.user.tools[item_id]['amount']))
            
        return x[page * self.items_per_page : (page + 1) * self.items_per_page]
    
    def get_options(self):
        options = []
        for i, item in enumerate(self.get_items_page(self.actual_page)):
            options.append(discord.SelectOption(label=item[0].name, value=str(i)))
        return options
    
    @dui.button(label='Anterior', style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = (len(self.user.tools.keys())-1)//self.items_per_page
            
        await self.update_embed(interaction)
        
    @dui.button(label='Proximo', style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page += 1
        if self.actual_page >= (len(self.user.tools.keys())+1)//self.items_per_page:
            self.actual_page = 0
            
        await self.update_embed(interaction)
    
    @dui.button(label='Enviar', style=discord.ButtonStyle.blurple, emoji='✉️')
    async def send(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode enviar os itens!', ephemeral=True)
            return
        if self.selected is None:
            await interaction.response.send_message('Selecione um item!', ephemeral=True)
            return
        
        self.stop()
        self.clear_items()
        await interaction.response.edit_message(view=None)
        
        # Remove item from user
        self.user.tools[[key for key in self.user.tools.keys()][self.selected]]['amount'] -= self.quantity
        if self.user.tools[[key for key in self.user.tools.keys()][self.selected]]['amount'] <= 0:
            del self.user.tools[[key for key in self.user.tools.keys()][self.selected]]
        
        # Add item to user2
        if self.user2.tools.get([key for key in self.user.tools.keys()][self.selected]) is None:
            self.user2.tools[[ key for key in self.user.tools.keys()][self.selected]] = {'amount': 0}
        self.user2.tools[[ key for key in self.user.tools.keys()][self.selected]]['amount'] += self.quantity
        
        # Update db
        self.client.db.update_value('users', 'data_user', self.user.id, self.user.save())
        self.client.db.update_value('users', 'data_user', self.user2.id, self.user2.save())
        self.client.db.save()
        await interaction.followup.send(f'Item enviado com sucesso para {self.user2_client.display_name}!', ephemeral=True)
        # Warn on user2 DM
        await self.user2_client.send(f'Voce recebeu ``{self.quantity}x {self.items.findById([key for key in self.user.tools.keys()][self.selected]).name}`` de {interaction.user.display_name}.')
    
    @dui.button(label='Fechar', style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.stop()
        self.clear_items()
        await interaction.response.edit_message(view=None)

class InventoryView(dui.View):
    def __init__(self, user:UserType, client:discord.Client):
        super().__init__()
        self.user = user
        self.client = client
        
        self.actual_page = 0
        self.items_per_page = 8
        self.items = ItemObj()
        
    def get_items_page(self, page:int) -> list:
        x = []
        for item_id in self.user.tools.keys():
            l:Item = self.items.findById(item_id)
            x.append((l, self.user.tools[item_id]['amount']))
            
        return x[page * self.items_per_page : (page + 1) * self.items_per_page]
    
    async def update_embed(self, interaction: discord.Interaction):
        e = discord.Embed(
            title='Inventário do usuário',
            color=0x00FF00
        )
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{(len(self.user.tools.keys())//self.items_per_page) + 1}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        
        items = self.get_items_page(self.actual_page)
        
        for i, item in enumerate(items):
            e.add_field(name=f"{i+1}. {str(item[0].name).capitalize()}", value=f"x``{item[1]}``", inline=False)
        await interaction.response.edit_message(embed=e, view=self)
    
    @dui.button(label='Anterior', style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = (len(self.user.tools.keys())-1)//self.items_per_page
            
        await self.update_embed(interaction)
        
        
    @dui.button(label='Proximo', style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page += 1
        if self.actual_page >= (len(self.user.tools.keys())+1)//self.items_per_page:
            self.actual_page = 0
            
        await self.update_embed(interaction)
        
    @dui.button(label='Fechar', style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.stop()
        self.clear_items()
        await interaction.response.edit_message(view=None)