from flask import Flask
from threading import Thread
import discord
import os

app = Flask('')

@app.route('/')
def home():
    return "Le Bot est en ligne!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Connecté en tant que {client.user}')

keep_alive()
client.run("token=token")