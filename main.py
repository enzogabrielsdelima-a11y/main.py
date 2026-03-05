import discord

from discord import app_commands

import requests

import os

from flask import Flask

from threading import Thread



# --- SISTEMA PARA MANTER ONLINE (KEEP ALIVE) ---

app = Flask('')



@app.route('/')

def home():

    return "Bot está vivo!"



def run():

    app.run(host='0.0.0.0', port=8080)



def keep_alive():

    t = Thread(target=run)

    t.start()



# --- CONFIGURAÇÃO DO BOT ---

class MyBot(discord.Client):

    def __init__(self):

        intents = discord.Intents.default()

        super().__init__(intents=intents)

        self.tree = app_commands.CommandTree(self)



    async def setup_hook(self):

        await self.tree.sync()

        print(f"Comandos sincronizados para {self.user}")



client = MyBot()



# --- COMANDO DO GOOGLE ---

@client.tree.command(name="google", description="Pesquisa algo no Google")

async def google(interaction: discord.Interaction, busca: str):

    # Dica: É melhor colocar essas chaves nas 'Environment Variables' da Render

    api_key = "SUA_CHAVE_API_AQUI" 

    cx = "SEU_ID_CX_AQUI"

    

    url = f"https://www.googleapis.com/customsearch/v1?key={api_key}&cx={cx}&q={busca}"

    

    await interaction.response.defer() # Faz o bot "pensar" para não dar timeout

    

    response = requests.get(url).json()

    

    if "items" in response:

        item = response['items'][0]

        titulo = item['title']

        link = item['link']

        snippet = item['snippet']

        

        embed = discord.Embed(title=titulo, url=link, description=snippet, color=0x4285F4)

        await interaction.followup.send(embed=embed)

    else:

        await interaction.followup.send("Não encontrei resultados para essa busca.")



# --- INICIALIZAÇÃO ---

keep_alive() # Liga o mini-servidor para a Render não desligar o bot



# Pega o token das variáveis de ambiente da Render (mais seguro)

token = os.environ.get('MTQ3Nzk1ODIzMDc0MjE0MzA4Ng.GrtP96.91-8yDLiB0-BpaG4HsXB4tR2hqqtsYFwr3uqgI') 

client.run(token)
