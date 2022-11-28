

import discord
import os
import openai
import requests as req

API_KEY = openai.api_key = os.getenv("OPENAI_API_KEY") 
TOKEN = os.getenv("OPENAI_DISCORD_BOT") 



def openai_anwser(question: str) -> str:
    """Takes a question as str pass it to openai to anwser then retur the anwser."""
    text = openai.Completion.create(
    model="text-davinci-002",
    prompt= f"{question}",
    temperature=0.9,
    max_tokens=2048,
    n = 1,
    )
    anwser = text["choices"][0]["text"].strip()

    return anwser

def openai_images(prompt:str):
    image = openai.Image.create(prompt=f"{prompt}", n=1, size="1024x1024")
    data : list = image["data"]

    for urls in data:
        url = urls["url"] 
        return url

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if "#ask " in message.content:
        q = message.content
        question = q.replace("#ask ", "")
        
        anwser = openai_anwser(question)
        print(f"{message.author} just used the bot to ask a question.")

        await message.channel.send(anwser)
    
    if "#image " in message.content:
        q = message.content
        prompt = q.replace("#image ", "")
        url = openai_images(prompt)

        print(f"{message.author} just used the bot to ask for an image.")
        await message.channel.send(url)

client.run(TOKEN)