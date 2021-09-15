import discord
from discord.ext import commands

################################
description = "A bot that helps approve members for our fb discord"

#!! these need to be set before running the code !!!
TOKEN = '[bot token here]'
MOD_CHANNEL_ID = 000000  # [mod channel id here]

# discord shtuff
client = discord.Client()
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix='$', description=description,  intents=intents)

mod_channel = client.get_channel(MOD_CHANNEL_ID)

# EMOJIS🥶🥶🥶🥶


def get_emoji_by_name(name: str) -> discord.Emoji:
    return [
        e
        for e in client.emojis
        if e.name == name
    ][0]


EMOJI_CHECKMARK = get_emoji_by_name('white_check_mark')
EMOJI_ENVELOPE = get_emoji_by_name('envelope')
EMOJI_QUESTION = get_emoji_by_name('question')


##################################################################


@client.event
async def on_reaction_add(reaction: discord.Reaction, user: discord.User):
    if reaction.message.channel != mod_channel or reaction.message.user != client.user:
        return
    if reaction.emoji == EMOJI_CHECKMARK:
        verified_message = "Your account has been verified and your access has been granted! Feel free to check any of the " \
            "verified channels now :-) "
        userino = reaction.message.mentions[0]
        role = discord.utils.get(reaction.message.guild.roles, name="verified")
        await userino.add_roles(role)
        await userino.send(verified_message)


@client.event
async def on_message(message):
    initial_greeting = """Hello! This is the verifier bot for the FB Interns discord.   
    
To make things easier for the mods and to accelerate the verification process, **please send a screenshot of your 
career profile that clearly states your full name, as well as the page where it says that you have been accepted to a 
2022 position.** 
  
After sending this, a moderator will review this and I will let you know when your access has been approved, 
or if further verification is required. 

If you need further assistance, please type `zuck help` so I can send someone 
your way. 

The mod team wishes you the best and hopes you have a successful 2022 internship!"""

    help_is_on_way = "Help is on the way! Please wait while one of our moderators contacts you. "

    notification_verify = "<@%s> has asked for the above image to be used as proof of verification. React with any " \
                          "emoji to this message to approve the user. " % message.author.id

    notification_help = "User <@%s> has asked for a mod to contact them for further discussion.  " % message.author.id

    if message.author == client.user:
        return
    elif len(message.attachments) != 0:
        await message.channel.send("Proof received. Mods will review it shortly :)")
        await mod_channel.send(message.attachments[0])
        last_message = await mod_channel.send(notification_verify)
        await last_message.add_reaction(EMOJI_CHECKMARK)
        await last_message.add_reaction(EMOJI_ENVELOPE)
    elif str(message.content).lower().startswith("$zuck verify"):
        await message.channel.send(initial_greeting)
    elif str(message.content).lower().startswith("$zuck help"):
        await message.channel.send(help_is_on_way)
        await mod_channel.send(notification_help)
    elif str(message.content).lower().startswith("$zuck"):
        await message.channel.send("I did not understand that. Please type `$zuck verify`, and then send the required "
                                   "screenshot, to help verify your account, or `$zuck help` to speak to a mod.")


client.run(TOKEN)
