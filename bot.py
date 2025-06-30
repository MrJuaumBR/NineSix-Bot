from data.config import *


# Funny Commands
@t.command(name='gaymeter', description='Vê o percentual de gayzice do usuário',guilds=[])
async def _gaymeter(interaction: discord.Interaction, user: discord.User = None):
    if user == None:
        user = interaction.user
    
    user_name = user.display_name
    
    # Count the vogals in name and the len of the name if the it have > 5 vogals = 50%, and if len > 7 = 100% it's linear
    percentage = 0
    vogals = 0
    for c in user_name:
        if c.lower() in 'aeiou':
            vogals += 1

    percentage += vogals/5 * 50
    percentage += len(user_name)/7 * 50
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
    
# Economy Commands
@t.command(name='dar-item', description='Entregue um item para o usuário',guilds=[])
async def _give_item(interaction: discord.Interaction, user: discord.User):
    if user == interaction.user: await interaction.response.send_message('Não é possível dar um item para si mesmo!', ephemeral=True)
    u = getUser(client, interaction.user.id)
    u2 = getUser(client, user.id)
    
    e = discord.Embed(
        title='Itens disponíveis no seu inventário',
        color=0x00FF00
    )
    
    v = GiveItemView(u,u2,user,interaction.client)
    for i, item in enumerate(u.tools.keys()):
        
        e.add_field(name=f"{i+1}. {Items.findById(item).name}", value=f"x``{u.tools[item]['amount']}``", inline=False)
    
    await interaction.response.send_message(embed=e, view=v)
    
@t.command(name='inventario', description='Vê o inventário do usuário',guilds=[])
async def _inventory(interaction: discord.Interaction):
    u = getUser(client, interaction.user.id)
    
    # View paginated
    v = InventoryView(u,interaction.client)
    e = discord.Embed(
        title='Inventário do usuário',
        color=0x00FF00
    )
    e.set_footer(text=f'Pág: {v.actual_page + 1}/{(len(v.user.tools.keys())//v.items_per_page) + 1}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
    for i, item in enumerate(v.get_items_page(v.actual_page)):
        e.add_field(name=f"{i+1}. {item[0].name}", value=f"x``{item[1]}``", inline=False)
    await interaction.response.send_message(embed=e, view=v)
    
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
        
    for i, item in enumerate(ss.get_items_page(ss.actual_page)):
        e.add_field(name=f"{i+1}. {item.name}", value=f"{item.description} - ``S${client.humanize_cash(item.price)}``", inline=False)
    
    v = UserShopView(ss, interaction.user, interaction.client)
    e.set_footer(text=f'Pág: {v.actual_page + 1}/{(len(v.shop.items)+1)//6}', icon_url=interaction.guild.icon or interaction.user.display_avatar)
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
        
    x = (random.randint((u.level+u.rep)*5, (u.level+u.rep)*7) * extra) * 100
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
            # Send a DM to the user that received the payment
            await user.send(f'Voce recebeu ``S${amount}`` de {interaction.user.display_name}.')
            await interaction.response.send_message(f'Pagou ``S${client.humanize_cash(amount)}`` para {user.mention}.', ephemeral=True)
        async def declinePayment(interaction: discord.Interaction):
            PayView.stop()
            await interaction.response.send_message(f'Pagamento para {user.mention} cancelado.', ephemeral=True)
        
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
        description=f'Experience multiplier: {str(s.server_exp_mult)}\nMoney multiplier: {str(s.server_money_mult)}\nTax: {str(s.server_tax)}%\nLevel up channel: {f'<#{s.level_up_channel}>' if s.level_up_channel != None else "None"}',
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
@t.command(name='cash-debug-add', description='Add cash to user | Only admin can use',guilds=[])
async def _add_cash(interaction: discord.Interaction, user_id: str, amount: int, local:Literal['bank', 'wallet'] = 'wallet'):
    if interaction.user.id in owner_ids:
        if user_id in ['0','me','i',None]:
            user_id = interaction.user.id
        if user_id != None:
            if amount != None:
                u = User(int(user_id), interaction.client)
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
                u = User(int(user_id), interaction.client)
                u.exp += exp
                pdb.database.update_value('users', 'data_user', int(user_id), u.save())
                pdb.database.save()
                await interaction.response.send_message('User exp set to ' + str(exp), ephemeral=True)
            else:
                await interaction.response.send_message('Exp not provided')
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