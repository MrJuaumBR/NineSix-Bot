# Geral
- Toda ferramenta e arma possui durabilidade, algumas tem durabilidade infinita, ou seja, são **Inquebráveis**
- Para usar as ferramentas é necessário possuir o nível delas, você pode as ter no inventário, mas não será capaz de utiliza-las.
- Algumas ações necessitam de ferramentas certas
- `/usuario-loja` é o local aonde você pode adquirir suas armas e ferramentas, é uma loja apenas para itens aplicáveis diretamente ao usuário.
- `/servidor-loja` é uma loja aplicável apenas ao servidor(ex: Multiplicador de experiência).
- Após comprar uma ferramenta/arma, você precisa equipa-la usando o comando `/equipamentos` e então ir até a página do respectivo equipamento.
- Se estiver curioso em relação aos itens, você pode olhar o `/catalogo` que irá te dar uma visão de todos os itens do bot.

![Discord Shield](https://discord.com/api/guilds/1014636634341392475/widget.png?style=shield)

# Servidores
- A cada mensagem que você envia você ganha uma pequena quantidade de **experiência** e de **dinheiro**
- você pode usar o comando ``/level-up-channel`` para definir aonde a mensagem de subida de nível será enviada.
- Os servidores podem ter taxas definidas pelo dono dele(Inclui transações e ...)<span id='servers-#1'>*¹</span>
- Certos comandos só podem ser executados por administradores, tenha certeza de por essa permissão somente em quem **confie**.

<small>
<a href="#servers-#1">*¹</a>: Pode(e deve) sofrer alterações futuramente
</small>

# Buscar
- A busca é uma ação útil para encontrar materiais básicos.
- A quantidade que vem dos itens é aleatório(1-3), bem como o item que vem.
- Tem um cooldown de 10 segundos.
- Os itens podem vir com qualquer nível.
- O comando é ``/buscar ``
<table>
    <caption>Itens que podem ser encontrados</caption>
    <tr>
        <th>
            Item
        </th>
        <th>
            Id
        </th>
    </tr>
    <tr>
        <td>
            Graveto
        </td>
        <td>
            wood_stick
        </td>
    </tr>
    <tr>
        <td>
            Pedra
        </td>
        <td>
            rock_stone
        </td>
    </tr>
    <tr>
        <td>
            Grama
        </td>
        <td>
            plant_grass
        </td>
    </tr>
    <tr>
        <td>
            Ervas
        </td>
        <td>
            plant_herbs
        </td>
    </tr>
    <tr>
        <td>
            Osso
        </td>
        <td>
            bone
        </td>
    </tr>
</table>

# Mineração
- Para minerar é necessário uma [picareta equipada](#geral)
- Você só pode minerar minérios que forem do seu nível ou inferiores.
- Ao minerar você gasta durabilidade da picareta.
- Para minerar use o comando ``/minerar`` e você pode por uma medida de nível(min, max).
<table>
    <caption>Picaretas</captions>
    <tr>
        <th>
            Item
        </th>
        <th>
            Nível
        </th>
        <th>
            Durabilidade
        </th>
        <th>
            Preço
        </th>
    </tr>
    <tr>
        <td>
            Picareta de Madeira(pickaxe_wood)
        </td>
        <td>
            Nvl. 1
        </td>
        <td>
            3
        </td>
        <td>
            100
        </td>
    </tr>
    <tr>
        <td>
            Picareta de Cobre(pickaxe_copper)
        </td>
        <td>
            Nvl. 1
        </td>
        <td>
            15
        </td>
        <td>
            500
        </td>
    </tr>
    <tr>
        <td>
            Picareta de Prata(pickaxe_silver)
        </td>
        <td>
           Nvl. 5
        </td>
        <td>
            45
        </td>
        <td>
            2.500
        </td>
    </tr>
    <tr>
        <td>
            Picareta de Ouro(pickaxe_gold)
        </td>
        <td>
            Nvl. 10
        </td>
        <td>
            200
        </td>
        <td>
            10.000
        </td>
    </tr>
    <tr>
        <td>
            Picareta de Diamante(pickaxe_diamond)
        </td>
        <td>
            Nvl. 15
        </td>
        <td>
            500
        </td>
        <td>
            50.000
        </td>
    </tr>
    <tr>
        <td>
            Picareta de Obsidian(pickaxe_obsidian)
        </td>
        <td>
            Nvl. 20
        </td>
        <td>
            <b>Inquebrável<b>
        </td>
        <td>
            1.000.000
        </td>
    </tr>
</table>

# Crafts
- Misturas devem ser craftadas e então forjadas(ex: Latão)
- Para abrir o menu de craft use ``/craft``
<table>
    <caption>Itens <i>Craftáveis</i></caption>
    <tr>
        <th>
            Item
        </th>
        <th>
            Nível
        </th>
        <th>
            Durabilidade
        </th>
        <th>
            Recursos
        </th>
    </tr>
    <tr>
        <td>
            3x Graveto(wood_stick)
        </td>
        <td>
            Nvl. 1
        </td>
        <td>
            *<span title="Inquebrável">Material</span>
        </td>
        <td>
            <ul>
                <li>
                    1x Madeira de Madeira(wood_oak)
                </li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            1x Porrete(weapon_club)
        </td>
        <td>
            Nvl. 1
        </td>
        <td>
            3
        </td>
        <td>
            <ul>
                <li>
                    3x Graveto(wood_stick)
                </li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            1x Faca de Cobre(weapon_copper_knife)
        </td>
        <td>
            Nvl. 1
        </td>
        <td>
            5
        </td>
        <td>
            <ul>
                <li>
                    1x Barra de Cobre(bar_copper)
                </li>
                <li>
                    1x Graveto(wood_stick)
                </li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            1x Faca de Prata(weapon_silver_knife)
        </td>
        <td>
            Nvl. 1
        </td>
        <td>
            7
        </td>
        <td>
            <ul>
                <li>
                    1x Barra de Prata(bar_silver)
                </li>
                <li>
                    1x Graveto(wood_stick)
                </li>
            </ul>
        </td>
    </tr>
        <tr>
        <td>
            3x Espinhos de Ferro(iron_spikes)
        </td>
        <td>
            Nvl. 10
        </td>
        <td>
            *<span title="Inquebrável">Material</span>
        </td>
        <td>
            <ul>
                <li>
                    1x Barra de Ferro(bar_iron)
                </li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            2x Minério de Latão(ore_brass)
        </td>
        <td>
            Nvl. 10
        </td>
        <td>
            *<span title="Inquebrável">Material</span>
        </td>
        <td>
            <ul>
                <li>
                    2x Minério de Cobre(ore_copper)
                </li>
                <li>
                    1x Minério de Ferro(ore_iron)
                </li>
            </ul>
        </td>
    </tr>
    <tr>
        <td>
            1x Porrete com Espinhos(weapon_club_spiked)
        </td>
        <td>
            Nvl. 10
        </td>
        <td>
            15
        </td>
        <td>
            <ul>
                <li>
                    1x Porrete(weapon_club)
                </li>
                <li>
                    1x Espinhos de Ferro(iron_spikes)
                </li>
            </ul>
        </td>
    </tr>
</table>

# Forja
- Para forjar qualquer minério é necessário ter **3 Minérios Brutos**
- Use o comando `/forjar` para forjar, o parâmetro _auto_ é usado para forjar todos os minérios possíveis automaticamente.
- Cada minério tem seu próprio nível para ser trabalhado, use o `/catalogo` para ver os níveis.
<table>
    <caption>Itens que podem ser forjados</caption>
    <tr>
        <th>
            Item
        </th>
        <th>
            Quantidade
        </th>
        <th>
            Resultado
        </th>
        <th>
            Nível
        </th>
    </tr>
    <tr>
        <td>
            Minério de estanho(ore_tin)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de estanho(bar_tin)
        </td>
        <td>
            Nvl. 1
        </td>
    </tr>
    <tr>
        <td>
            Minério de cobre(ore_copper)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de cobre(bar_copper)
        </td>
        <td>
            Nvl. 1
        </td>
    </tr>
    <tr>
        <td>
            Minério de prata(ore_silver)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de prata(bar_silver)
        </td>
        <td>
            Nvl. 1
        </td>
    </tr>
    <tr>
        <td>
            Minério de Ferro(ore_iron)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de ferro(bar_iron)
        </td>
        <td>
            Nvl. 10
        </td>
    </tr>
    <tr>
        <td>
            Minério de latão(ore_brass)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de latão(bar_brass)
        </td>
        <td>
            Nvl. 10
        </td>
    </tr>
    <tr>
        <td>
            Minério de ouro(ore_gold)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de ouro(bar_gold)
        </td>
        <td>
            Nvl. 10
        </td>
    </tr>
    <tr>
        <td>
            Diamante(ore_diamond)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de Diamante(bar_diamond)
        </td>
        <td>
            Nvl. 15
        </td>
    </tr>
    <tr>
        <td>
            Obsidiana(ore_obsidian)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de obsidian(bar_obsidian)
        </td>
        <td>
            Nvl. 20
        </td>
    </tr>
    <tr>
        <td>
            Minério de Manasteel(ore_manasteel)
        </td>
        <td>
            3x
        </td>
        <td>
            Barra de Manasteel(bar_manasteel)
        </td>
        <td>
            Nvl. 25
        </td>
    </tr>
</table>

# Habilidades
- Para equipar sua habilidade use ``/equipamentos``
- Para desequipar uma habilidade apenas clique para equipar uma que já esteja equipada
- Você pode ter até 5 Habilidades equipadas
- Libere-as com nível.
- Encontre-as.

???

# Inimigos
- Os inimigos aparecem apenas se eles estiverem dentro do seu alcance de nível.
- Os ataques dos inimigos podem acertar, ou não.
- Os inimigos podem dropar alguns itens.
- Use ``/batalhar`` para lutar com um inimigo.
- Ao perder uma batalha você recebera penalidades.

<table>
    <caption>Inimigos</caption>
    <thead>
        <td>
            Nome
        </td>
        <td>
            Nível
        </td>
        <td>
            Drops
        </td>
        <td>
            Ataques
        </td>
    </thead>
    <tbody>
        <tr>
            <td>
                Goblin(goblin_basic)
            </td>
            <td>
                Nvl. 1
            </td>
            <td>
                <ul>
                    <li>Osso: 50%</li>
                    <li>Tecido: 30%</li>
                    <li>Couro: 20%</li>
                </ul>
            </td>
            <td>
                <ul>
                    <li>Soco</li>
                    <li>Chute</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>
                Goblin Gigante(goblin_giant)
            </td>
            <td>
                Nvl. 5
            </td>
            <td>
                <ul>
                    <li>Osso: 30%</li>
                    <li>Tecido: 40%</li>
                    <li>Couro: 30%</li>
                </ul>
            </td>
            <td>
                <ul>
                    <li>Soco</li>
                    <li>Chute</li>
                </ul>
            </td>
        </tr>
        <tr>
            <td>
                Skeleton(skeleton_basic)
            </td>
            <td>
                Nvl. 5
            </td>
            <td>
                <ul>
                    <li>Osso: 100%</li>
                </ul>
            </td>
            <td>
                <ul>
                    <li>Soco</li>
                    <li>Investida</li>
                </ul>
            </td>
        </tr>
    </tbody>
</table>