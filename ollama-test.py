"""
Disclaimer: This is a test file to test ollama responses, it is not part of the bot.
! Probably will not be implemented, but who knows?

* I need a good AI for NPCs
"""

import random, json, requests, subprocess
from ollama import chat, ChatResponse

model:str = 'gemma2:9b' #llama3.1:8b, openchat:7b

def check_ollama_status():
    response = requests.get('http://localhost:11434/')
    if response.status_code == 200:
        return True
    else:
        return False

if not check_ollama_status():
    print("Ollama is offline, starting it...")
    subprocess.run(f"ollama run {model} &", shell=True)
    
npcs_data = json.load(open('data/npcs.json', 'r'))

npcs_names = [x for x in npcs_data['npcs'].keys()]

def response_generator(nome_usuario,mensagem_usuario):
    npc = random.choice(npcs_names)

    npc_data = npcs_data['npcs'][npc]
    
    relations_npcs = ''
    for npc_name in npcs_names:
        if str(npc_name).lower() in str(npc_data['relations']).lower():
            rnpc = npcs_data['npcs'][npc_name]
            relations_npcs += f'- {npc_name}: \n\t- Idade: {rnpc['age']}\n\t- Genero: {rnpc["gender"]}\n\t- Ocupação: {rnpc["occupation"]}\n\t- Aparência: {rnpc["appearance"]}\n\t- Backstory: {rnpc["backstory"]}\n\t- Personalidade: {rnpc["personallity"]}\n\t- Relações: {rnpc["relations"]}\n\t- Frases Chaves: {rnpc["phrases"]}\n'
    prompt = f"""
    Este chat é para um sistema de NPCs que desenvolvi para meu bot no discord, aonde existe uma possibilidade do bot responder com algum NPC que foi criado a uma mensagem do usuario, por favor siga estas instruções a risca para que tudo funcione corretamente!
    O bot em questão é um bot com sistema de RPG medieval, mas não quero ações alguma, apenas falas!
    é Obrigatório que a resposta seja em português, e que ela seja coerente com a personalidade do NPC e seguindo regras do português.
    o chat tem que me retornar apenas o que o NPC falaria, sem mais nada, absolutamente mais nada.
    
    [CONTEXTO DO MUNDO DO BOT]
    {npcs_data['context']}
    [INSTRUÇÕES]
    - Responda APENAS com a fala do NPC, SEM narração, *ações* ou metadados.
    - Use *portugues brasileiro* informal (como uma pessoa real falaria).
    - A resposta deve refletir a personalidade, backstory e relações do NPC.
    - Sempre responda com frases curtas(menos de 20 palavras).
    - Mantenha suas respostas de forma coerente com a personalidade do NPC e seguindo regras do portugues.

    [DADOS DO NPC]
    - Nome: {npc} 
    - Idade: {npc_data['age']}
    - Gênero: {npc_data['gender']}
    - Ocupação: {npc_data['occupation']}
    - Aparência: {npc_data['appearance']}
    - Backstory: {npc_data['backstory']}
    - Personalidade: {npc_data['personallity']}
    - Relações: {npc_data['relations']}
    - Frases Chaves: {npc_data['phrases']}
    - Formas de Expressão: {npc_data['language']}

    [Dados dos NPCs relacionados]
    Os itens a seguir são os NPCs relacionados ao NPC atual, use  as informações deles apenas quando necessário, não misture com o restante das informações do NPC.
    {relations_npcs}

    [DIÁLOGO ATUAL]
    Nome do usuário: "{nome_usuario}"
    Usuário: "{mensagem_usuario}"

    [NPC]:"""  # <– A resposta deve começar AQUI, SEM prefixos como "Thiago:".
    r:ChatResponse = chat(model=model, messages=[
        {
            'role': 'user',
            'content': prompt
        }
    ])
    
    return npc,r['message']['content']

while True:
    mensagem_usuario = str(input('>'))
    if mensagem_usuario == 'exit':
        if check_ollama_status():
            print("Stopping ollama...")
            subprocess.run(f"ollama stop {model}", shell=True)
        break
    else:
        npc, msg =response_generator('Thiago',mensagem_usuario)
        print(f'[{npc}]: {msg}')