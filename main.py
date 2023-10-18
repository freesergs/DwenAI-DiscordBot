import discord
from discord.ext import commands
import openai as novaai
import json

from keep_alive import keep_alive
keep_alive()

# Initialize your bot
bot_token = "Discord Bot Token"
intents = discord.Intents.default()
intents.typing = False
intents.presences = False
bot = commands.Bot(command_prefix='!', intents=intents)

# Set the NOVA AI API base and key
novaai.api_base = 'https://api.nova-oss.com/v1'
novaai.api_key = 'NovaAI API key'


# Dictionary to track conversations with users
user_conversations = {}

@bot.event
async def on_ready():
  print(f'Logged in as {bot.user.name}')

  # Set the bot's custom status
  custom_status = discord.CustomActivity(name="'!dwen @DwenAI' to interact!")
  await bot.change_presence(activity=custom_status)

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  # Avoid responding to ourselves

    if message.content.startswith('!dwen'):
        user_message = message.content[6:]  # Remove the command prefix
        user_id = message.author.id

        # Get the conversation for this user or create a new one
        if user_id in user_conversations:
            conversation = user_conversations[user_id]
        else:
            conversation = []
            user_conversations[user_id] = conversation

        conversation.append(f"User: {user_message}")

        # Send user's message to NOVA AI API and get a response
        response = get_nova_response(user_message)

        conversation.append(f"Bot: {response}")

        await message.channel.send(response)



def get_nova_response(user_message):
    # Prepare the message as per the API documentation
    messages = [{"role": "user", "content": user_message}]

    # Make a request to NOVA AI API
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
