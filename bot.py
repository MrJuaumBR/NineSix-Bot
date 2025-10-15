from data.config import *


# Funny Commands
@t.command(name='dado', description='Jogue um dado',guilds=[])
async def _roll(interaction: discord.Interaction, sides: int = 6, times: int = 1, fix: int = 0):
    rolled:list[int,] = [random.randint(1, sides) for i in range(times)]
    text = f'Você jogou um dado ({times}d{sides} {"" if fix in [0, None, ''] else f"+{fix}"}) e caiu: \n['
    final_sum = 0
    for i,r in enumerate(rolled):
        if i != len(rolled) - 1:
            text += f'{r+fix}{"" if fix in [0, None, ''] else f" ({r}+{fix})"}, '
        else:
            text += f'{r+fix}{"" if fix in [0, None, ''] else f" ({r}+{fix})"}'
        final_sum += r+fix
        
    text += f'\nSoma: {final_sum}'
    await interaction.response.send_message(text)

@t.command(name='gaymeter', description='Vê o percentual de gayzice do usuário',guilds=[])
async def _gaymeter(interaction: discord.Interaction, user: discord.User = None):
    if user == None:
        user = interaction.user
    
    user_name = user.display_name
    
    # Count the vowels in name and the len of the name if the it have > 5 vowels = 50%, and if len > 7 = 100% it's linear
    percentage = 0
    vowels = 0
    for c in user_name:
        if c.lower() in 'aeiou':
            vowels += 1

    percentage += vowels/5 * 50 # Importance: 50%
    percentage += len(user_name)/7 * 50 # Importance: 50%
    if percentage > 100:
        percentage = 100
    
    gay_titles = [
        'Hétero', # 0% <=
        'Hétero Moderno', # 20% <=
        'Bisexual', # 40% <=
        'Bixinha', # 60% <=
        'Bixa', # 80% <=
        'Gazela', # 100%
    ]
    
    e = discord.Embed(
        title='Gaymeter',
        description=f'Gaymeter de {user_name}: {str(round(percentage))}% 🏳️‍🌈\nPode ser considerado: **{gay_titles[min(5, max(0, int(percentage / 20)))]}**',
        color=Funny_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=user.display_avatar)
    await interaction.response.send_message(embed=e)

@t.command(name='casal', description=' Vê a porcentagem de compatibilidade de casais',guilds=[])
async def _casal(interaction: discord.Interaction, user1: discord.User, user2: discord.User=None):
    if user2 == None: user2 = interaction.user
    if user1 == user2: await interaction.response.send_message('Não pode ser o mesmo usuário!', ephemeral=True)
    
    names = [normalize_text(user1.display_name), normalize_text(user2.display_name)]
    vogals = [sum(1 for ltr in name if ltr.lower() in 'aeiou') for name in names]
    
    percentage = (vogals[0]/vogals[1])/2 + (len(names[0])/len(names[1]))/2
    percentage -= abs((vogals[0]-vogals[1])+(len(names[0])-len(names[1])))/100
    if percentage > 1: percentage -= 1
    percentage = min(100, max(0, round(percentage*100,2)))
    
    couple_titles = [
        'Colegas', #<= 0
        'Amigos', #<= 20
        'Companheiros', #<= 40
        'Namorados', #<= 60
        'Noivos', #<= 80
        'Casados' #<= 100
    ]
    
    e = discord.Embed(
        title=f'Compatibilidade de {user1.display_name} e {user2.display_name}',
        description=f'Compatibilidade: {str(percentage)}%\nPodem ser considerados: **{couple_titles[min(5, max(0, int(percentage / 20)))]}**',
        color=Funny_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=user1.display_avatar)
    await interaction.response.send_message(embed=e)


# RPG Commands
@t.command(name='batalhar',description='Batalha contra monstros aleatórios',guilds=[])
async def _batalhar(interaction: discord.Interaction):
    u = getUser(client, interaction.user.id)
    enemy:Enemy = CHandler.getRandomEnemyNew(level=u.level)
    
    v = BattleView(client, u, enemy)
    
    await interaction.response.send_message(embed=v.embed(interaction), view=v)

@t.command(name='status', description='Vê o todos os status do usuário',guilds=[])
async def _status(interaction: discord.Interaction, user: discord.User = None):
    if user == None: user = interaction.user
    u = getUser(client, user.id)
    
    life, maxLife = u.get_life_info()
    mana, maxMana = u.get_mana_info()
    # Will display: Banco, Carteira, Reputação, Nível, quantos itens, quantas habilidades, experiência e porcentagem, vida e porcentagem e etc...
    e = discord.Embed(
        title='Status',
        description=f"""
        Banco: ``${client.humanize_cash(u.bank)}``
        Carteira: ``${client.humanize_cash(u.wallet)}``
        Reputação: ``{u.rep}``
        Nível: ``{int(u.level)} - {u.exp}/{u.level*100} ({round((u.exp/(u.level*100))*100,2)}%)``
        Quantidade de itens: ``{u.getTotalItems()}``
        Quantidade de habilidades: ``{u.getTotalSkills()}``
        Vida: ``{int(life)}/{int(maxLife)} ({round(life/maxLife*100,2)}%)``
        Mana: ``{int(mana)}/{int(maxMana)} ({round(mana/maxMana*100,2)}%)``""",
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=user.display_avatar or interaction.guild.icon)
    await interaction.response.send_message(embed=e)

@t.command(name='lutar', description='Lute contra usuários',guilds=[])
async def _lutar(interaction: discord.Interaction):
    await interaction.response.send_message('...')

@t.command(name='criar-party', description='Crie uma party',guilds=[])
async def _criar_party(interaction: discord.Interaction):
    await interaction.response.send_message('...')
    
@t.command(name='convidar-party', description='Entre em uma party',guilds=[])
async def _convidar_party(interaction: discord.Interaction):
    await interaction.response.send_message('...')
    
@t.command(name='party', description='Vê a party',guilds=[])
async def _party(interaction: discord.Interaction):
    await interaction.response.send_message('...')

@t.command(name='catalogo', description='Vê o catalogo de itens',guilds=[])
async def _catalogo(interaction: discord.Interaction, category: ItemsTypes = None):
    u = getUser(client, interaction.user.id)
    
    v = CatalogView(u, client, category)
    e = discord.Embed(
            title=f'Catalogo de itens {f"({str(category).capitalize()})" if category != None else ""}',
            description=f'Com este comando você pode ver **todos** os itens do bot.\nTotal de itens: ``{len(RawItems.getAll())}``',
            color=0x00FF00
    )
    e.set_footer(text=f'Pág: {v.actual_page + 1}/{math.ceil(len(RawItems.getAll(category))/v.items_per_page)}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
    v.create_fields(e, v.actual_page)
    
    await interaction.response.send_message(embed=e, view=v)
# Economy Commands
@t.command(name='pescar', description='Pescar',guilds=[])
@discord.app_commands.checks.cooldown(1, 3)
async def _fish(interaction: discord.Interaction):
    # Get the user info
    u = getUser(client, interaction.user.id)
    
    # Get the tool: fishing_rod
    tool = u.getEquipped('fishing_rod')
    
    if tool == None:
        await interaction.response.send_message('Você precisa ter uma **vara de pesca** equipada para usar este comando, caso não tenha, use o comando `/usuario-loja` e compre uma.', ephemeral=True)
        return
    
    if tool['usages'] <= 0:
        u.deleteTool('fishing_rod')
    
    fish = RawItems.getCategory('fish',level_limit=u._level)
    fish:Item = random.choice(fish)
    e = discord.Embed(
        title='Pescando',
        description=f'Voce pescou um {fish.name}!',
        color=Funny_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=interaction.guild.icon or interaction.user.display_avatar)
    if tool['item_data']['unbreakable'] == False:
        tool['usages'] -= 1 
        if tool['usages'] <= 0:
            u.deleteTool('fishing_rod')
            await interaction.followup.send('Sua vara de pesca foi quebrada, use o comando `/usuario-loja` e compre uma nova.', ephemeral=True)
        
    u.add_item(fish.id, 1)
    client.db.update_value('users', 'data_user', u.id, u.save())
    client.db.save()
    
    await interaction.response.send_message(embed=e)
    
@t.command(name='forjar', description='Transforme seus minérios em barras!',guilds=[])
async def _smelt(interaction: discord.Interaction, auto: bool = False):
    u = getUser(client, interaction.user.id)
    
    if auto:
        ores = u.getItems(subtype='ore')
        if len(ores) == 0:
            await interaction.response.send_message('Vocês precisa ter pelo menos **minerado** algo.', ephemeral=True)
            return
        ores = [ore for ore in ores if ore['amount'] >= 3]
        if len(ores) == 0:
            await interaction.response.send_message('Você não consegue forjar nada atualmente.', ephemeral=True)
            return
        else:
            text = f'Você forjou:\n'
            for ore in ores:
                quantity = ore['amount']//3
                u.remove_item(ore['item_data']['id'], quantity*3)
                bar = RawItems.findById(f'{str(ore['item_data']["id"]).replace("ore_","bar_")}')
                u.add_item(bar.id, quantity)
                text += f'* {quantity}x {bar.name}\n'
            
            client.db.update_value('users', 'data_user', u.id, u.save())
            client.db.save()
            e = discord.Embed(
                title='Forjando',
                description=text,
                color=discord.Color.dark_gray()
            )
            await interaction.response.send_message(embed=e)
            return
    else:
        ores = u.getItems(subtype='ore')
        if len(ores) == 0: 
            await interaction.response.send_message('Vocês precisa ter pelo menos **minerado** algo.', ephemeral=True)
            return
        ores = [x for x in ores if x['amount'] >= 3]
        if len(ores) == 0: 
            await interaction.response.send_message('Vocês precisa ter pelo menos 3x minérios brutos para forjar.', ephemeral=True)
            return
        
        v = SmeltView(u, client, ores, BotCrafts)
        await interaction.response.send_message(embed=v.embed(interaction), view=v)
        return

@t.command(name="loja-diaria", description='Vê a loja diária do usuário',guilds=[])
async def _daily_shop(interaction: discord.Interaction):
    random.seed(datetime.now().day + datetime.now().year)
    daily_shop_id = random.randint(0, len(BotDailyShop)-1)
    daily_shop = BotDailyShop[daily_shop_id]
    
    u = getUser(client, interaction.user.id)
    v = DailyShop(u, client, daily_shop)
    
    await interaction.response.send_message(embed=v.embed(interaction), view=v)
    
@t.command(name='minerar', description='Minerar',guilds=[])
async def _mine(interaction: discord.Interaction,min_level: int = 0, max_level: int = 0):
    # Get the user info
    u = getUser(client, interaction.user.id)
    
    # Get the tool: pickaxe
    tool = u.getEquipped('pickaxe')
    
    if tool == None:
        await interaction.response.send_message('Vocês precisa ter uma **picareta** equipada para usar este comando, caso não tenha, use o comando `/usuario-loja` e compre uma.', ephemeral=True)
        return
    
    if tool['usages'] <= 0:
        u.deleteTool('pickaxe')
    
    if min_level < 0:
        min_level = 0
    if max_level > u.level:
        max_level = u._level
    if min_level > max_level:
        await interaction.response.send_message('O nível mínimo deve ser menor que o máximo.', ephemeral=True)
        return
    
    if min_level == 0 and max_level == 0:
        max_level = u._level
        min_level = 0
        
    mineral = RawItems.getSubtype('ore', exclude=['ore_brass'], level_range=(min_level, max_level))
    mineral:Item = random.choice(mineral)
    e = discord.Embed(
        title='Minerando',
        description=f'Voce minerou um {mineral.name}!',
        color=Funny_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=interaction.guild.icon or interaction.user.display_avatar)
    if tool['item_data']['unbreakable'] == False:
        tool['usages'] -= 1 
        if tool['usages'] <= 0:
            u.deleteTool('pickaxe')
            await interaction.followup.send('Sua picareta foi quebrada, use o comando `/usuario-loja` e compre uma nova.', ephemeral=True)
    
    u.add_item(mineral.id, 1)
    client.db.update_value('users', 'data_user', u.id, u.save())
    client.db.save()
    
    await interaction.response.send_message(embed=e)

@t.command(name='craft', description='Transforme seus itens!',guilds=[])
async def _craft(interaction: discord.Interaction):
    u = getUser(client, interaction.user.id)
    v = CraftView(u, client, BotCrafts)
    
    await interaction.response.send_message(embed=v.embed(interaction), view=v)
    
@t.command(name='buscar',description='Busca materiais na região',guilds=[])
@discord.app_commands.checks.cooldown(1, 10)
async def _search(interaction: discord.Interaction):
    findable:list[Item,] = RawItems.getFindable()
    item = random.choice(findable)
    amount = random.randint(1,3)
    e = discord.Embed(
        title='Buscando',
        description=f'Voce encontrou x{amount} {item.name}!',
        color=Funny_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=interaction.guild.icon or interaction.user.display_avatar)
    
    u = getUser(client, interaction.user.id)
    u.add_item(item.id, amount)
    
    client.db.update_value('users', 'data_user', u.id, u.save())
    client.db.save()
    await interaction.response.send_message(embed=e)

@t.command(name='derrubar', description='Obtenha madeira ao cortar arvores',guilds=[])
async def _cut(interaction: discord.Interaction):
    u = getUser(client, interaction.user.id)
    
    woods = RawItems.getSubtype('wood', level_limit=u._level)
    
    wood = random.choice(woods)
    amount = random.randint(1,3)
    e = discord.Embed(
        title='Cortando',
        description=f'Voce cortou x{amount} {wood.name}!',
        color=Funny_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=interaction.guild.icon or interaction.user.display_avatar)
    
    u.add_item(wood.id, amount)
    
    client.db.update_value('users', 'data_user', u.id, u.save())
    client.db.save()
    await interaction.response.send_message(embed=e)
    
@t.command(name='suporte', description='Suporte',guilds=[])
async def _support(interaction: discord.Interaction):
    await interaction.response.send_message('Suporte')

@t.command(name='equipamentos', description='Vê os equipamentos do usuário e permite equipa-los.',guilds=[])
async def _equipamentos(interaction: discord.Interaction):
    u = getUser(client, interaction.user.id)
    
    v = GearView(u,interaction.client)
    
    e = v.embed(interaction)
    
    await interaction.response.send_message(embed=e, view=v)
    
@t.command(name='dar-item', description='Entregue um item para o usuário',guilds=[])
async def _give_item(interaction: discord.Interaction, user: discord.User):
    if user == interaction.user: await interaction.response.send_message('Não é possível dar um item para si mesmo!', ephemeral=True)
    u = getUser(client, interaction.user.id)
    u2 = getUser(client, user.id)
    
    v = GiveItemView(u,u2,user,interaction.client)
    e = v.embed(interaction)
    
    await interaction.response.send_message(embed=e, view=v)
    
@t.command(name='inventario', description='Vê o inventário do usuário',guilds=[])
async def _inventory(interaction: discord.Interaction, category: ItemsTypes= None):
    u = getUser(client, interaction.user.id)
    
    # View paginated
    v = InventoryView(u,interaction.client, category)
    
    await interaction.response.send_message(embed=v.embed(interaction), view=v)
    
@t.command(name='usuario-loja', description='Compre itens para o usuário',guilds=[])
async def _user_shop(interaction: discord.Interaction):
    ss = UserShop()
    ss.items.clear()
    for i in User_Items:
        ss.add_item(i)
        
    e = discord.Embed(
        title='Loja do usuário',
        description=f'Itens a venda para o usuário:\n*Dinheiro do banco será utilizado para comprar itens*\n',
        color=Economy_Color
    )
        
    
    v = UserShopView(ss, interaction.user, interaction.client)
    v.create_fields(e, v.actual_page)
    e.set_footer(text=f'Pág: {v.actual_page + 1}/{math.ceil(len(v.shop.items)+1)/6}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
    await interaction.response.send_message(embed=e, view=v,ephemeral=True)

@t.command(name='roubar', description='Roube o dinheiro do usuário',guilds=[])
async def _steal(interaction: discord.Interaction, user: discord.User):
    if user == interaction.user: await interaction.response.send_message('Não é possível roubar a si mesmo!', ephemeral=True)
    
    await interaction.response.send_message(f'Mó preguiça de fazer')

@t.command(name='diario', description='Colete seu dinheiro diariamente - 24Hrs',guilds=[])
@discord.app_commands.checks.cooldown(1, 86400)
async def _daily(interaction: discord.Interaction):
    u = getUser(client, interaction.user.id)
    s = getServer(client, interaction.guild.id)
    
    extra = 1.0
    
    if 'daily_buff' in s.buffs.keys():
        extra += s.buffs['daily_buff']
        
    x = (random.uniform((u.level+u.rep)*5, (u.level+u.rep)*7) * extra) * 100
    u.wallet += x
    client.db.update_value('users', 'data_user', u.id, u.save())
    client.db.save()
    await interaction.response.send_message(f'Voce coletou ``S${client.humanize_cash(round(x,2))}`` do seu diário!')

@t.command(name='trabalhar', description='Trabalhe para ganhar dinheiro - 8Hrs',guilds=[])
@discord.app_commands.checks.cooldown(1, 28800)
async def _work(interaction: discord.Interaction):
    u = getUser(client, interaction.user.id)
    s = getServer(client, interaction.guild.id)
    
    works = [
        'Caixa',
        'Gari',
        'Garçom',
        'Mecanico',
        'Uber',
        'Entregador',
        'Pedreiro'
    ]
    
    extra = 1.0
    
    if 'work_buff' in s.buffs.keys():
        extra += s.buffs['work_buff']
        
    x = (random.randint((u.level+u.rep)*5, (u.level+u.rep)*7) * extra) * 10
    u.wallet += x
    client.db.update_value('users', 'data_user', u.id, u.save())
    client.db.save()
    await interaction.response.send_message(f'Voce trabalhou de {random.choice(works)} ganhou ``S${client.humanize_cash(round(x,2))}``!')

@t.command(name='pagar', description='Pague dinheiro para o usuário',guilds=[])
async def _pay(interaction: discord.Interaction, user: discord.User, amount: float, local:Literal['bank', 'wallet'] = 'wallet'):
    if user != None:
        u = getUser(client, user.id)
        x = getUser(client, interaction.user.id)
        if amount > (x.wallet if local == 'wallet' else x.bank):
            await interaction.response.send_message(f'Dinheiro insuficiente {"na carteira" if local == "wallet" else "no banco"}.', ephemeral=True)
            return
        e = discord.Embed(
            title='Pagamento',
            description=f'Você deseja pagar ``S${client.humanize_cash(amount)}`` para {user.mention}?',
            color=Economy_Color
        )
        PayView = discord.ui.View()
        async def acceptPayment(interaction: discord.Interaction):
            u.wallet += amount
            if local == 'bank':
                x.bank -= amount
            else:
                x.wallet -= amount
            client.db.update_value('users', 'data_user', user.id, u.save())
            client.db.update_value('users', 'data_user', interaction.user.id, x.save())
            client.db.save()
            PayView.stop()
            PayView.clear_items()
            # Send a DM to the user that received the payment
            await interaction.edit_original_response(view=PayView)
            await user.send(f'Voce recebeu ``S${amount}`` de {interaction.user.display_name}.')
            await interaction.response.send_message(f'Pagou ``S${client.humanize_cash(amount)}`` para {user.mention}.', ephemeral=True)
        async def declinePayment(i2: discord.Interaction):
            PayView.stop()
            PayView.clear_items()
            await interaction.edit_original_response(view=PayView)
            await i2.response.send_message(f'Pagamento para {user.mention} cancelado.', ephemeral=True)
        
        acceptButton = discord.ui.Button(label='Pagar 👍', style=discord.ButtonStyle.green, custom_id='y')
        declineButton = discord.ui.Button(label='Pagar 👎', style=discord.ButtonStyle.red, custom_id='n')
        acceptButton.callback = acceptPayment
        declineButton.callback = declinePayment
        PayView.add_item(acceptButton)
        PayView.add_item(declineButton)
        await interaction.response.send_message(embed=e, view=PayView)
        
@t.command(name='saldo', description='Vê o saldo do usuário',guilds=[])
async def _balance(interaction: discord.Interaction, user: discord.User = None):
    if user == None: user = interaction.user
    cdb = pyDatabase('./data/database').db()
    u = User(user.id, interaction.client).load(cdb.findByText('users', 'id', user.id)['data_user'])
    
    e = discord.Embed(
        title='Saldo do usuário',
        description=f'Dinheiro na carteira: ``S${str(u.wallet)}``\nDinheiro no banco: ``S${client.humanize_cash(u.bank)}``\nTotal: ``S${client.humanize_cash(u.wallet + u.bank)}``\nReputação: ``{client.humanize_cash(u.rep)}``',
        color=Economy_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=user.display_avatar)
    
    await interaction.response.send_message(embed=e)

@t.command(name='depositar', description='Deposite dinheiro na sua conta',guilds=[])
async def _deposit(interaction: discord.Interaction, amount: float):
    cdb = pyDatabase('./data/database').db()
    u = User(interaction.user.id, interaction.client).load(cdb.findByText('users', 'id', interaction.user.id)['data_user'])
    if amount > u.wallet:
        await interaction.response.send_message('Dinheiro insuficiente na carteira.', ephemeral=True)
        return
    u.bank += amount
    u.wallet -= amount
    cdb.update_value('users', 'data_user', interaction.user.id, u.save())
    cdb.save()
    await interaction.response.send_message(f'Depositou ``S${amount}`` a sua conta do banco.', ephemeral=True)
    
@t.command(name='sacar', description='Saque dinheiro da sua conta',guilds=[])
async def _withdraw(interaction: discord.Interaction, amount: float):
    cdb = pyDatabase('./data/database').db()    
    u = User(interaction.user.id, interaction.client).load(cdb.findByText('users', 'id', interaction.user.id)['data_user'])
    if amount > u.bank:
        await interaction.response.send_message('Dinheiro insuficiente no banco.', ephemeral=True)
        return
    u.bank -= amount
    u.wallet += amount
    cdb.update_value('users', 'data_user', interaction.user.id, u.save())
    cdb.save()
    await interaction.response.send_message(f'Sacou ``S${amount}`` da sua conta do banco.', ephemeral=True)

# Level Commands
@t.command(name='nivel', description='Vê o nível do usuário',guilds=[])
async def _level(interaction: discord.Interaction, user: discord.User = None):
    if user == None: user = interaction.user
    cdb = pyDatabase('./data/database').db()
    u = User(user.id, interaction.client).load(cdb.findByText('users', 'id', user.id)['data_user'])
    
    e = discord.Embed(
        title='Nível do usuário',
        description=f'Nível: {str(u.level)}\nExperiência: {str(round(u.exp,2))}/{str(round(u.level*100,2))}({str(round((u.exp/(u.level*100))*100,2))}%)',
        color=Level_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=user.display_avatar)
    await interaction.response.send_message(embed=e)

# Server Owner Commands
@discord.app_commands.checks.has_permissions(administrator=True)
@t.command(name='servidor-loja',description='Compre itens para o servidor',guilds=[])
async def _shop(interaction: discord.Interaction):
    s = getServer(client, interaction.guild.id)
    
    items = ''
    ss = ServerShop()
    for i in Server_Items:        
        ss.add_item(i)
    
    
    e = discord.Embed(
        title='Servidor Shop',
        description=f'Itens a venda para o servidor:\n*Dinheiro do banco será utilizado para comprar itens*\n',
        color=Economy_Color        
    )
        
    for i, item in enumerate(ss.get_items_page(ss.actual_page)):
        e.add_field(name=f"{i+1}. {item.name}", value=f"{item.description} - ``S${item.price}``", inline=False)
    
    v = ServerShopView(ss, interaction.user, interaction.client)
    e.set_footer(text=f'Pág: {v.actual_page + 1}/{(len(v.shop.items)+1)//5}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
    await interaction.response.send_message(embed=e, view=v)
    
    
@discord.app_commands.checks.has_permissions(administrator=True)
@t.command(name='server-info', description='Get server info | Only admin can use',guilds=[])
async def _server_info(interaction: discord.Interaction):
    s = Server(interaction.guild.id).load(pdb.database.findByText('servers', 'id', interaction.guild.id)['data_server'])
    
    e = discord.Embed(
        title='Server info',
        description=f'Multiplicador de Experiência: {str(s.server_exp_mult)}\nMultiplicador de Dinheiro: {str(s.server_money_mult)}\nTaxa(%): {str(round(s.server_tax*100,2))}%\nCanal de Level Up: {f'<#{s.level_up_channel}>' if s.level_up_channel != None else "None"}\nNº de Membros: {str(interaction.guild.member_count)}',
        color=Debug_Color
    )
    e.set_footer(text=str(random.choice(tips)), icon_url=interaction.guild.icon or interaction.user.display_avatar)
    await interaction.response.send_message(embed=e)

@discord.app_commands.checks.has_permissions(administrator=True)
@t.command(name='level-up-channel', description='Set level up channel | Only admin can use',guilds=[])
async def _level_up_channel(interaction: discord.Interaction, channel: discord.TextChannel):
    
    s = Server(interaction.guild.id)
    s.level_up_channel = channel.id
    client.db.update_value('servers', 'data_server', interaction.guild.id, s.save())
    client.db.save()
    
    await interaction.response.send_message('Level up channel set to ' + channel.mention)

# Bot Owner Commands
@t.command(name='attacks-debug-add', description='Add attack to database | Only admin can use',guilds=[])
async def _add_attack(interaction: discord.Interaction, attack_id: str, user_id:str=None):
    if interaction.user.id in owner_ids:
        if user_id == None:
            user_id = interaction.user.id
        
        u = getUser(client, user_id)
        u.add_attack(attack_id)
        pdb.database.update_value('users', 'data_user', user_id, u.save())
        pdb.database.save()
        await interaction.response.send_message('Attack added to user', ephemeral=True)

@t.command(name='cash-debug-add', description='Add cash to user | Only admin can use',guilds=[])
async def _add_cash(interaction: discord.Interaction, user_id: str, amount: int, local:Literal['bank', 'wallet'] = 'wallet'):
    if interaction.user.id in owner_ids:
        if user_id in ['0','me','i',None]:
            user_id = interaction.user.id
        if user_id != None:
            if amount != None:
                u = getUser(client, int(user_id))
                if local == 'bank':
                    u.bank += amount
                elif local == 'wallet':
                    u.wallet += amount
                pdb.database.update_value('users', 'data_user', int(user_id), u.save())
                pdb.database.save()
                await interaction.response.send_message('User ' + local + ' added ' + str(amount), ephemeral=True)
            else:
                await interaction.response.send_message('Amount not provided')
@t.command(name='lvl-debug-exp', description='Set user exp | Only admin can use',guilds=[])
async def _set_exp(interaction: discord.Interaction, user_id: str, exp: int):
    if interaction.user.id in owner_ids:
        if user_id in ['0','me','i',None]:
            user_id = interaction.user.id
        if user_id != None:
            if exp != None:
                u = getUser(client, int(user_id))
                u.exp += exp
                pdb.database.update_value('users', 'data_user', int(user_id), u.save())
                pdb.database.save()
                await interaction.response.send_message('User exp set to ' + str(exp), ephemeral=True)
            else:
                await interaction.response.send_message('Exp not provided')
        else:
            await interaction.response.send_message('User id not provided')
            
@t.command(name='db-debug-give-item', description='Give item to user | Only admin can use',guilds=[])
async def _give_item(interaction:discord.Interaction, item_id:str, user_id: str=None, amount:int=1):
    if interaction.user.id in owner_ids:
        if user_id in ['0','me','i',None]:
            user_id = interaction.user.id
        if user_id != None:
            if amount != None:
                u = getUser(client, int(user_id))
                if RawItems.findById(item_id):
                    u.add_item(item_id, amount)
                    pdb.database.update_value('users', 'data_user', int(user_id), u.save())
                    pdb.database.save()
                    await interaction.response.send_message('User ' + item_id + ' added ' + str(amount), ephemeral=True)
                else:
                    await interaction.response.send_message('Item not found')
            else:
                await interaction.response.send_message('Amount not provided')
        else:
            await interaction.response.send_message('User id not provided')
            
@t.command(name='db-debug-remove-user', description='Remove user from database | Only admin can use',guilds=[])
async def _remove_user(interaction: discord.Interaction, user_id: str):
    db = pdb.database
    user_id = int(user_id)
    if interaction.user.id in owner_ids:
        if user_id != None:
            if db.findByText('users', 'id', user_id):
                db.delete_values('users', user_id, ['id', 'data_user'])
                db.save()
                await interaction.response.send_message('User removed from database')
            else:
                await interaction.response.send_message('User not found in database')
        else:
            await interaction.response.send_message('User id not provided')
    else:
        await interaction.response.send_message('You are not authorized to use this command')

@t.command(name='db-debug-output-console', description='Output database to console | Only admin can use',guilds=[])
async def _output_console(interaction: discord.Interaction):
    if interaction.user.id in owner_ids:
        pdb.get_content()
        await interaction.response.send_message('Database output to console')
    else:
        await interaction.response.send_message('You are not authorized to use this command')

client.run(os.environ.get("TOKEN"))