import discord
from discord import ui as dui
from .User import User as UserType
from .Shop import ItemObj, Item
from typing import Literal

from ..globals import ItemsTypes, math, RawItems, GetEmoji

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
    
    def total_pages(self) -> int:
        total_items = self.user.getTotalItems()
        total_pages = math.ceil(total_items/self.items_per_page)
        if total_items % self.items_per_page > 0 and total_items > self.items_per_page:
            if not len(self.get_items_page(total_pages+1)) <= 0:
                total_pages += 1
            
        return int(total_pages)
    
    def get_items_indexes(self, page:int) -> tuple[int, int]:
        start_on:int = int(page * self.items_per_page)
        end_on:int = int((page + 1) * (self.items_per_page if self.user.getTotalItems() % self.items_per_page > 0 else self.items_per_page - int(self.user.getTotalItems() % self.items_per_page)))
        return start_on, end_on
    
    def get_items_info(self) -> list[tuple[Item, int]]:
        x = []
        for item in self.user.getItems():
            i = RawItems.findById(item['item_data']['id'])
            x.append((i, self.user.findItem(i.id)['amount']))
        return x
    
    def get_items_page(self, page:int) -> list[tuple[Item, int]]:
        x = self.get_items_info()
        start_on, end_on = self.get_items_indexes(page)
        return x[start_on : end_on]
    
    def embed(self, interaction:discord.Interaction):
        e = discord.Embed(
            title='Dar Item',
            description=f'Itens do seu inventário(``{self.user.getTotalItems()}``):',
            color=0x00FF00
        )
        
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{self.total_pages()}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        
        self.create_fields(e, self.actual_page)
        
        return e
    
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
    
    def create_fields(self, embed:discord.Embed, page:int):
        items = self.get_items_page(page)
        
        for i, item in enumerate(items):
            tool:Item = self.user.getItemById(item[0].id)
            embed.add_field(name=f"{i+1}. {item[0].name}", value=f"x``{item[1]}``\n{(f'Usos ``{self.client.humanize_number(tool["usages"])}`` restantes.' if not tool['item_data']['unbreakable'] else 'Este item é inquebrável!')}", inline=False)
    
    async def update_embed(self, interaction: discord.Interaction, react_type:Literal['next', 'back'] = 'next'): 
        self.remove_item(self.UiItemSelected)
        self.remove_item(self.UiItemQuantity)
        self.UiItemQuantity = dui.Select(placeholder='Quant.', options=[discord.SelectOption(label=f'{i}', value=f'{i}', default=(i == self.quantity)) for i in range(1,6,1)], min_values=1, max_values=1)
        self.UiItemQuantity.callback = self.UiItemQuantityCallback
        self.add_item(self.UiItemQuantity)
        self.UiItemSelected = dui.Select(placeholder='Selecione um item', options=self.get_options(), min_values=1, max_values=1)
        self.UiItemSelected.callback = self.UiItemSelectedCallback
        self.add_item(self.UiItemSelected)
        
        e = self.embed(interaction)
        
        await interaction.response.edit_message(embed=e, view=self)
    
    def get_options(self):
        options = []
        if len(self.get_items_page(self.actual_page)) == 0:
            options.append(discord.SelectOption(label='Nenhum item', value='0', default=True))
        else:
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
            self.actual_page = self.total_pages()-1
            
        await self.update_embed(interaction)
        
    @dui.button(label='Proximo', style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page += 1
        if self.actual_page >= self.total_pages():
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
        self.user.remove_item([key for key in self.user.tools.keys()][self.selected], self.quantity)
        
        # Add item to user2
        self.user2.add_item([key for key in self.user.tools.keys()][self.selected], self.quantity)
        
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
    def __init__(self, user:UserType, client:discord.Client, filter_category:ItemsTypes=None):
        super().__init__()
        self.user = user
        self.client = client
        
        self.actual_page = 0
        self.items_per_page = 8
        self.items = ItemObj()
        self.filter_category = filter_category
        self.user_items_ids = [key for key in self.user.tools.keys()] + [key for key in self.user.items.keys()]
        # Funcionando até aqui
    def total_pages(self) -> int:
        total_items = self.user.getTotalItems(self.filter_category)
        total_pages = math.ceil(total_items/self.items_per_page)
        if total_items % self.items_per_page > 0 and total_items > self.items_per_page:
            total_pages += 1
        return int(total_pages)
    def get_items_page(self, page:int) -> list:
        x = []
        for item_id in self.user_items_ids:
            if self.filter_category is None:
                l:Item = self.items.findById(item_id)
                x.append((l, self.user.findItem(item_id)['amount']))
            else:
                l:Item = self.items.findById(item_id)
                if l.item_type == self.filter_category:
                    x.append((l, self.user.findItem(item_id)['amount']))
        total_pages = math.ceil(len(x) / self.items_per_page)
        page = min(page, total_pages - 1)  # Ensure page number is within bounds
        return x[page * self.items_per_page : (page + 1) * self.items_per_page]
    
    def create_fields(self, embed:discord.Embed, page:int):
        items = self.get_items_page(page)
        
        if len(items) == 0:
            embed.add_field(name='Inventário vazio', value='Nenhum item encontrado.', inline=False)
            return
        for i, item in enumerate(items):
            uItem:Item = self.user.getItemById(item[0].id)
            d = ''
            if uItem['item_data']['item_type'] in ['material']:
                d = '\n``Este item é um material.``'
            elif uItem['item_data']['unbreakable']:
                d = '\n``Este item é inquebrável!``'
            else:
                d = f'\nUsos ``{self.client.humanize_number(uItem["usages"])}`` restantes.'
            formatted_item_text = f'x``{item[1]}``{d}'
            embed.add_field(name=f"{i+1}. {GetEmoji(item[0].id)}{str(item[0].name).capitalize()}", value=formatted_item_text, inline=False)
    
    def embed(self, interaction:discord.Interaction):
        e = discord.Embed(
            title='Inventário do usuário',
            color=0x00FF00
        )
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{self.total_pages()}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        
        self.create_fields(e, self.actual_page)
        return e
    
    async def update_embed(self, interaction: discord.Interaction):
        e = self.embed(interaction)
        
        await interaction.response.edit_message(embed=e, view=self)
    
    @dui.button(label='Anterior', style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = self.total_pages()-1
            
        await self.update_embed(interaction)
        
        
    @dui.button(label='Proximo', style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page += 1
        if self.actual_page >= self.total_pages():
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
        
class GearView(dui.View):
    def __init__(self, user:UserType, client:discord.Client):
        super().__init__()
        self.user = user
        self.client = client
        
        self.actual_page = 0
        
        self.pages = []
        self.create_pages()
        
        self.items = ItemObj()
        self.selected = None
        self.UiSelect = None
        if len(self.get_items_page(self.actual_page)) > 0:
            self.UiSelect = dui.Select(placeholder='Selec. um item para equipar.', options=self.get_options(), min_values=1, max_values=1)
            self.UiSelect.callback = self.UiSelectCallback
            self.add_item(self.UiSelect)        
        
        
    def create_pages(self):
        # Fishing Page 1/?
        self.pages.append({
            'description': 'Equipamentos de pesca',
            'items': self.user.getToolsByType('fishing_rod'),
            'item_type': 'fishing_rod'
        })
        # Mining Page 2/?
        self.pages.append({
            'description': 'Equipamentos de mineração',
            'items': self.user.getToolsByType('pickaxe'),
            'item_type': 'pickaxe'
        })
        # Axe Page 3/?
        self.pages.append({
            'description': 'Equipamentos de corte de madeira',
            'items': self.user.getToolsByType('axe'),
            'item_type': 'axe'
        })
        # Weapons Page 4/?
        self.pages.append({
            'description': 'Equipamentos de arma',
            'items': self.user.getToolsByType('weapon'),
            'item_type': 'weapon'
        })
        
    def get_items_page(self, page:int) -> list:
        return self.pages[page]['items']
    
    def get_options(self) -> list[discord.SelectOption]:
        return [discord.SelectOption(label=str(item['item_data']['name']).capitalize(), value=str(item['item_data']['id'])) for item in self.get_items_page(self.actual_page)]
    
    async def UiSelectCallback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return

        self.selected = str(self.UiSelect.values[0])
        await interaction.response.defer()
    def get_left_usages(self, item_id):
        item = self.user.getToolById(item_id)
        if item is None:
            return ""
        if item['item_data']['unbreakable']:
            return "Este item é inquebrável!"
        else:
            return f"Usos restantes: {item['usages']}."
    
    def actual_equipment(self):
        return f'{self.user.getEquipped(self.pages[self.actual_page]['item_type'])['item_data']['name']}\n{self.get_left_usages(self.user.getEquipped(self.pages[self.actual_page]['item_type'])['item_data']['id'])}'
    
    def create_fields(self, e:discord.Embed, page:int):
        items = self.get_items_page(page)
        if len(items) == 0:
            e.add_field(name='Nenhum item encontrado.', value='Nenhum item encontrado.', inline=False)
        else:
            for i, item in enumerate(items):
                e.add_field(name=f"{i+1}. {str(item['item_data']['name']).capitalize()}", value=f"x``{self.user.getToolById(item['item_data']['id'])['amount']}``\n{self.get_left_usages(item['item_data']['id'])}", inline=False)
    
    async def update_embed(self, interaction: discord.Interaction):
        self.selected = None
        if self.UiSelect:
            self.remove_item(self.UiSelect)
        if len(self.get_items_page(self.actual_page)) > 0:
            self.UiSelect = dui.Select(placeholder='Selec. um item para equipar.', options=self.get_options(), min_values=1, max_values=1)
            self.UiSelect.callback = self.UiSelectCallback
            self.add_item(self.UiSelect)
        
        e = discord.Embed(
            title='Equipamentos',
            description=f'{self.pages[self.actual_page]['description']}\nEquipado atualmente: {self.actual_equipment() if self.user.getEquipped(self.pages[self.actual_page]['item_type']) != None else "Nenhum"}.',
            color=0x00FF00
        )
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{len(self.pages)}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        self.create_fields(e, self.actual_page)
        await interaction.response.edit_message(embed=e, view=self)
        
    @dui.button(label='Anterior', style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = len(self.pages)-1
            
        await self.update_embed(interaction)
        
        
    @dui.button(label='Proximo', style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page += 1
        if self.actual_page >= len(self.pages):
            self.actual_page = 0
            
        await self.update_embed(interaction)
        
    @dui.button(label='Equipar', style=discord.ButtonStyle.green, emoji='🛠️')
    async def equip(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        
        if len(self.user.getToolsByType(self.pages[self.actual_page]['item_type'])) <= 0:
            await interaction.response.send_message('Você não possui nenhum item desta categoria.', ephemeral=True)
            return
        elif self.selected == None or self.selected == self.user.getEquipped(self.pages[self.actual_page]['item_type']):
            self.user.unequip(self.pages[self.actual_page]['item_type'])
            await interaction.response.send_message('Item desequipado.', ephemeral=True)
            return
        
        
        self.user.equip(self.pages[self.actual_page]['item_type'],self.selected)
        self.client.db.update_value('users', 'data_user', self.user.id, self.user.save())
        self.client.db.save()
        
        await interaction.response.defer()
        await interaction.followup.send('Item equipado.', ephemeral=True)
        await self.update_embed(interaction)
    
    @dui.button(label='Fechar', style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.stop()
        self.clear_items()
        await interaction.response.edit_message(view=None)
        
    
class CatalogView(dui.View):
    def __init__(self, user:UserType,client:discord.Client, filter_category:ItemsTypes=None):
        super().__init__()
        self.user = user
        self.client = client
        
        self.actual_page = 0
        self.items_per_page = 9
        self.filter_category = filter_category
    
    def get_items_page(self, page:int):
        return [item for item in RawItems.getAll(self.filter_category)][page * self.items_per_page : (page + 1) * self.items_per_page]
    
    def create_fields(self, e:discord.Embed, page:int):
        items = self.get_items_page(page)
        
        for i, item in enumerate(items):
            e.add_field(name=f"{i+1}. {GetEmoji(item.id)}{item.name}", value=f"Nível: **{item.level}**\n{item.description}", inline=True)
    
    async def update_embed(self, interaction:discord.Interaction):
        e = discord.Embed(
            title=f'Catalogo de itens {f"({str(self.filter_category).capitalize()})" if self.filter_category != None else ""}',
            description=f'Com este comando você pode ver **todos** os itens do bot.\nTotal de itens: ``{len(RawItems.getAll(self.filter_category))}``',
            color=0x00FF00
        )
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{math.ceil(len(RawItems.getAll(self.filter_category))/self.items_per_page)}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        self.create_fields(e, self.actual_page)
        await interaction.response.edit_message(embed=e, view=self)
    
    @dui.button(label='Anterior', style=discord.ButtonStyle.green)
    async def back(self, interaction: discord.Interaction, button: dui.button):
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = math.ceil(len(RawItems.getAll(self.filter_category))/self.items_per_page)
            
        await self.update_embed(interaction)
        
    @dui.button(label='Proximo', style=discord.ButtonStyle.green)
    async def next(self, interaction: discord.Interaction, button: dui.button):
        self.actual_page += 1
        if self.actual_page >= math.ceil(len(RawItems.getAll(self.filter_category))/self.items_per_page):
            self.actual_page = 0
            
        await self.update_embed(interaction)
        
class SmeltView(dui.View):
    local:str = 'smelt'
    def __init__(self, user:UserType,client:discord.Client, ores:list, crafts:dict):
        super().__init__()
        self.user = user
        self.client = client
        self.crafts = crafts
        
        self.actual_page = 0
        self.items_per_page = 8
        self.ores = ores
        
        self.UiSelect = None
        self.selected = []
        if len(self.ores) > 0:
            self.UiSelect = dui.Select(placeholder='Selec. os minérios.', options=self.get_options(), min_values=1, max_values=len(self.ores))
            self.UiSelect.callback = self.UiSelectCallback
            self.add_item(self.UiSelect)
            
    
    def get_items_page(self, page:int):
        return [ore for ore in self.ores][page * self.items_per_page : (page + 1) * self.items_per_page]
    def get_options(self):
        return [discord.SelectOption(label=ore['item_data']['name'], value=ore['item_data']['id']) for ore in self.ores]
    
    async def UiSelectCallback(self, interaction: discord.Interaction):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return

        self.selected = self.UiSelect.values
        await interaction.response.defer()
    
    def create_fields(self, e:discord.Embed, page:int):
        items = self.get_items_page(page)
        
        for i, item_data in enumerate(items):
            item = RawItems.findById(item_data['item_data']['id'])
            e.add_field(name=f"{i+1}. {GetEmoji(item.id)}{item.name}", value=f'Nível: **{item.level}**\n``x{self.user.getItemById(item.id)['amount']}``', inline=True)
    def embed(self, interaction:discord.Interaction):
        # Update Select Ui
        self.remove_item(self.UiSelect)
        self.UiSelect = dui.Select(placeholder='Selec. os minérios.', options=self.get_options(), min_values=1, max_values=len(self.ores))
        self.UiSelect.callback = self.UiSelectCallback
        self.add_item(self.UiSelect)
        
        e = discord.Embed(
            title=f'Forja',
            description=f'O que você deseja forjar?\nTotal de itens: ``{len(self.ores)}``',
            color=0x00FF00
        )
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{math.ceil(len(self.ores)/self.items_per_page)}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        self.create_fields(e, self.actual_page)
        return e
    
    async def update_embed(self, interaction:discord.Interaction):
        await interaction.response.edit_message(embed=self.embed(interaction), view=self)
    
    @dui.button(label='Anterior', style=discord.ButtonStyle.gray)
    async def back(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = math.ceil(len(self.ores)/self.items_per_page)
            
        await self.update_embed(interaction)
    
    @dui.button(label='Próximo', style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page += 1
        if self.actual_page >= math.ceil(len(self.ores)/self.items_per_page):
            self.actual_page = 0
            
        await self.update_embed(interaction)
        
    @dui.button(label='Forjar', style=discord.ButtonStyle.green)
    async def smelt(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        forged_items:str = f''
        for ind, item_data in enumerate(self.selected):
            item = RawItems.findById(item_data)
            crafted = RawItems.getOreBar(item.id)
            craft_amount = int(self.user.getItemById(item.id)['amount']/3)
            self.user.remove_item(item.id, craft_amount*3)
            self.user.add_item(crafted, craft_amount)
            forged_items += f'``x{craft_amount}`` {item.name} -> {RawItems.findById(crafted).name.capitalize()}{"\n" if ind < len(self.selected)-1 else ""}'
        
        emb = discord.Embed(
            title='Forja',
            description=f'Você forjou:\n{forged_items}',
            color=0x00FF00            
        )
        self.client.db.update_value('users', 'data_user', self.user.id, self.user.save())
        self.client.db.save()
        self.clear_items()
        self.stop()
        await interaction.response.edit_message(embed=emb, view=self)
    
    
    @dui.button(label='Fechar', style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.clear_items()
        self.stop()
        await interaction.response.edit_message(view=None)
    
class CraftView(dui.View):
    local:str = 'craft'
    def __init__(self, user:UserType, client:discord.Client, crafts:dict):
        super().__init__()
        self.user = user
        self.client = client
        self.rawCrafts = crafts
        self.rawCrafts_keys = list(self.rawCrafts.keys())
        
        self.crafts = {}
        self.craft_data:dict = {} # This will get all the data from rawCrafts
        self.crafts_load()
        
        self.crafts_per_page = 9
        self.actual_page = 0
        self.selected:str = None # Id
        self.quantity:int = 1
        
        self.UiItemSelect = dui.Select(placeholder="Selec. o que deseja criar...", options=self.get_options_page(self.actual_page), min_values=1, max_values=1)
        self.UiItemSelect.callback = self.UiItemSelectCallback
        self.add_item(self.UiItemSelect)
        
        self.UiSelectQuantity = dui.Select(placeholder='Quant.', options=[discord.SelectOption(label='0', value='0', default=True)], min_values=1, max_values=1,disabled=True)
        self.UiSelectQuantity.callback = self.UiItemQuantityCallback
        self.add_item(self.UiSelectQuantity)
        
    async def UiItemSelectCallback(self, interaction:discord.Interaction):
        self.selected = self.UiItemSelect.values[0]
        
        self.remove_item(self.UiSelectQuantity)
        self.UiSelectQuantity = dui.Select(placeholder='Quant.', options=[discord.SelectOption(label=f'{i}', value=f'{i}', default=(i == self.quantity)) for i in range(1, self.get_max_quantity(self.selected)+1, 1)], min_values=1, max_values=1,disabled=False)
        self.UiSelectQuantity.callback = self.UiItemQuantityCallback
        self.add_item(self.UiSelectQuantity)
        
        self.craft_data = self.rawCrafts[self.selected]
        
        await self.update_embed(interaction)

    async def UiItemQuantityCallback(self, interaction:discord.Interaction):
        self.quantity = self.UiSelectQuantity.values[0]
        await interaction.response.defer()
    
    def get_max_quantity(self, item_id:int):
        if item_id in self.rawCrafts.keys():
            items = self.rawCrafts[item_id]['items']
            return min(self.user.getItemById(i['id'])['amount'] // i['amount'] for i in items)
        
        return 0
    def crafts_load(self):
        
        for key in self.rawCrafts_keys:
            if RawItems.findById(key) and self.rawCrafts[key]['local'] == self.local: self.crafts[key] = RawItems.findById(key)
        
    def get_crafts_page(self, page:int):
        return list(self.crafts.keys())[page * self.crafts_per_page : (page + 1) * self.crafts_per_page]
    
    def get_options_page(self, page:int) -> list[discord.SelectOption]:
        r = []
        for l in self.get_crafts_page(page):
            if RawItems.canCraft(self.user, l):
                r.append(discord.SelectOption(label=RawItems.findById(l).name, value=l, default=(True if self.selected == l else False)))
        
        return (r if len(r) > 0 else [discord.SelectOption(label='Nenhum item disponível', value='none', default=True)])
    
    def create_fields(self, e:discord.Embed, page:int):
        crafts = self.get_crafts_page(page)
        if len(crafts) == 0:
            e.add_field(name='Nenhum item encontrado.', value='Nenhum item encontrado.', inline=False)
        else:
            for i, item_data in enumerate(crafts):
                item = RawItems.findById(item_data)
                required_items = '\n- '.join([f'{RawItems.findById(i["id"]).name} x{i["amount"]}' for i in self.rawCrafts[item_data]['items']])
                e.add_field(name=f"{i+1}. {GetEmoji(item.id)}{item.name}{'(Faltam recursos.)' if not RawItems.canCraft(self.user, item.id) else ''}", value=f'Items: ```\n- {required_items}```\nVocê tem ``x{self.user.getItemById(item.id)['amount'] if self.user.getItemById(item.id) else 0}``\n``{self.craft_data["result"]}`` por crafting.\nNível: **{item.level}**', inline=True)
    
    def embed(self, interaction:discord.Interaction):
        e = discord.Embed(title='Crafting', color=0x00FF00)
        self.create_fields(e, self.actual_page)
        e.set_footer(text=f'Pág: {self.actual_page + 1}/{math.ceil(len(self.crafts)/self.crafts_per_page)}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
        return e
    
    async def update_embed(self, interaction:discord.Interaction):
        self.remove_item(self.UiItemSelect)
        self.UiItemSelect = dui.Select(placeholder="Selec. o que deseja criar...", options=self.get_options_page(self.actual_page), min_values=1, max_values=1)
        self.UiItemSelect.callback = self.UiItemSelectCallback
        self.add_item(self.UiItemSelect)
        
        self.remove_item(self.UiSelectQuantity)
        self.UiSelectQuantity = dui.Select(placeholder='Quant.', options=[discord.SelectOption(label=f'{i}', value=f'{i}', default=(i == self.quantity)) for i in range(1, (self.get_max_quantity(self.selected)+1 if self.get_max_quantity(self.selected)+1 < 6 else 6), 1)] if not self.get_max_quantity(self.selected) == 0 else [discord.SelectOption(label='0', value='0', default=True)], min_values=1, max_values=1,disabled=False if self.get_max_quantity(self.selected) > 0 else True)
        self.UiSelectQuantity.callback = self.UiItemQuantityCallback
        self.add_item(self.UiSelectQuantity)
        
        await interaction.response.edit_message(embed=self.embed(interaction), view=self)
    
    @dui.button(label='Anterior', style=discord.ButtonStyle.gray)
    async def back(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page -= 1
        if self.actual_page < 0:
            self.actual_page = math.ceil(len(self.crafts)/self.crafts_per_page) - 1
            
        await self.update_embed(interaction)
        
    @dui.button(label='Próximo', style=discord.ButtonStyle.gray)
    async def next(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.actual_page += 1
        if self.actual_page >= math.ceil(len(self.crafts)/self.crafts_per_page) - 1:
            self.actual_page = 0
            
        await self.update_embed(interaction)
    @dui.button(label='Criar', style=discord.ButtonStyle.green)
    async def create(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        for item in self.rawCrafts[self.selected]['items']:
            self.user.remove_item(item['id'], int(item['amount'] * self.quantity))
        self.user.add_item(self.selected, int(self.quantity) * self.craft_data['result'])
        
        self.client.db.update_value('users', 'data_user', self.user.id, self.user.save())
        self.client.db.save()
        
        await interaction.response.send_message(f'Você fez ``{self.quantity}x`` {RawItems.findById(self.selected).name}', ephemeral=True)
        await self.update_embed(interaction)
        
    
    @dui.button(label='Fechar', style=discord.ButtonStyle.red)
    async def close(self, interaction: discord.Interaction, button: dui.button):
        if interaction.user.id != self.user.id:
            await interaction.response.send_message('Apenas o dono do inventário pode interagir!', ephemeral=True)
            return
        self.clear_items()
        self.stop()
        await interaction.response.edit_message(view=self)