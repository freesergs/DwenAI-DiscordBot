import discord
from discord.ext import commands
import openai as novaai
import os

from keep_alive import keep_alive
keep_alive()

# Initialize your bot
bot_token = os.environ.get("DISCORD_BOT_TOKEN")
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Set the NOVA AI API base and key
novaai.api_base = os.environ.get("NOVA_API_BASE")
novaai.api_key = os.environ.get("NOVA_API_KEY")

# Dictionary to track conversations with users
user_conversations = {}

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    custom_status = discord.Game('!dwen @DwenAI to interact!')
    await bot.change_presence(activity=custom_status)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Avoid responding to ourselves

    if message.content.startswith('!dwen'):
        user_message = message.content[6:]  # Remove the command prefix
        user_id = message.author.id

        if user_id in user_conversations:
            conversation = user_conversations[user_id]
        else:
            conversation = []
            user_conversations[user_id] = conversation

        # Include a system message to set the AI identity
        messages = [
            {"role": "system", "content": "DwenAI."},
            {"role": "user", "content": user_message}
        ]

        conversation.append(f"User: {user_message}")

        # Send the messages to the NOVA AI API and get a response
        response = get_nova_response(messages)

        conversation.append(f"DwenAI: {response}")

        await message.channel.send(response)

        # Handle questions about the developer
        if "who made" in user_message.lower() or "who developed" in user_message.lower():
            await message.channel.send(".")

def get_nova_response(messages):
    try:
        response = novaai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages
        )

        return response['choices'][0]['message']['content']
    except Exception as e:
        print(f"Error from NOVA AI API: {str(e)}")
        return "An error occurred while processing your request."

# Start the bot
bot.run(bot_token)
