import os
from dotenv import load_dotenv
import discord
from discord.ext import commands

load_dotenv()

################################
description = "A bot that helps approve members for our fb discord"
TOKEN = str(os.getenv('DISCORD_TOKEN'))
MOD_CHANNEL_ID = int(os.getenv('MOD_CHANNEL_ID'))

# EMOJIS🥶🥶🥶🥶
EMOJI_CHECKMARK = '✅'
EMOJI_ENVELOPE = '✉️'
EMOJI_EYES = '👀'

# discord stuff
client = discord.Client()
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

################################
# MESSAGES #

# Reactions to verify user
BOT_NAME = "zuck"

VERIFIED_MESSAGE = "Your account has been verified and your access has been granted! Feel free to check " \
                   "any of the verified channels now :-) "
FURTHER_VERIFICATION = "The mod team would like to ask a couple questions about your verification proof. " \
                       "\nDon't worry! A mod will be with you soon.\n\nRemember, you can also dm the mods " \
                       "with `$%s dm_mods` + the message you want to send! " % BOT_NAME

DOES_NOT_SATISFY = "Mods received your proof, but cannot verify you at this time. " \
                   "REASON: *Please make sure you have accepted your offer __prior__ to verification and " \
                   "that there is a checkmark for this on your new hire checklist.*"

# DMing Bot
INITIAL_GREETING = """Hello! This is the verifier bot for the FB Interns discord.   

To make things easier for the mods and to accelerate the verification process, **please reply here with a screenshot 
of your __new hire checklist__ and your full name in the right top corner (so you may need to click on the dropdown box). 

Important: __You must have already accepted your offer for your verified status to be granted!__** 

After sending this, a moderator will review this and I will let you know when your access has been approved, 
or if further verification is required. 

If you need further assistance, please type `$%s dm_mods` so I can send someone your way. You may choose to send a 
custom message to the mods by typing said message right after `$%s dm_mods`. 

The mod team wishes you the best and hopes you have a successful 2022 internship!""" % (BOT_NAME, BOT_NAME)

HELP_IS_ON_WAY = "Help is on the way! Please wait while one of our moderators contacts you. "

PROOF_RECEIVED = "Proof received. Mods will review it shortly :)"

COMMAND_HELP = "Commands:  `$%s verify` to get verification instructions. `$%s dm_mods` to speak to a mod. You " \
               "may choose to send a custom message to the mods by typing said message right after command " \
               "`$%s dm_mods`. " % (BOT_NAME, BOT_NAME, BOT_NAME)

INVALID_COMMAND = "Beep, boop, I did not get that. "

# Notifying mods about user
NOTIFICATION_VERIFY = "<@%s> has asked for the above image to be used as proof of verification. React with %s to " \
                      "approve the user, %s to let them know you will be contacting them for further info, or %s " \
                      "if they have not yet accepted offer."

NOTIFICATION_HELP = "User <@%s> has asked for a mod to contact them for further discussion.  "

BOT_JOKE_PHRASE = "I asked my developers to make a better version of JS. I knew this was a huge " \
                  "thing to ask - but looking back, they did React pretty well!"


################################

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_reaction_add(reaction, _user):
    """
    Help mods attribute "verified" role by simply clicking on a react button
    :param _user: [unused param]
    :param reaction: a reaction object to the message. Includes
        - reaction.count , the amount of people having reacted with this emoji
        - reaction.message , the message object within the reaction (see param of on_message for more info)
            - reaction.message.mentions , helping us identify the user tagged in the message, if any
    """
    if reaction.count > 1 and reaction.message.mentions and reaction.message.channel.id == MOD_CHANNEL_ID:
        userino = reaction.message.mentions[0]
        if str(reaction.emoji) == EMOJI_CHECKMARK:
            role = discord.utils.get(reaction.message.guild.roles, name="verified")
            await userino.add_roles(role)
            await userino.send(VERIFIED_MESSAGE)

        elif str(reaction.emoji) == EMOJI_ENVELOPE:
            await userino.send(FURTHER_VERIFICATION)

        elif str(reaction.emoji) == EMOJI_EYES:
            await userino.send(DOES_NOT_SATISFY)


@client.event
async def on_message(message):
    """
    The core exchange between bot and a user
    :param message: the message object sent to the bot. Includes
        - message.channel
        - message.content (the string of a message)
        - message.attachments , a list of attachments such as a picture, a link, etc
        - message.author , the user object that sent the message
    """
    mod_channel = client.get_channel(MOD_CHANNEL_ID)

    if message.author == client.user:
        return
    if message.content.startswith("$%s tell me a joke" % BOT_NAME):  # little easter egg
        await message.channel.send(BOT_JOKE_PHRASE)

    elif isinstance(message.channel, discord.channel.DMChannel):
        # send proof to mod channel, notify mods, and offer reaction options
        if len(message.attachments) != 0:
            await message.channel.send(PROOF_RECEIVED)
            await mod_channel.send(message.attachments[0])
            last_message = await mod_channel.send(NOTIFICATION_VERIFY % (message.author.id,
                                                                         EMOJI_CHECKMARK,
                                                                         EMOJI_ENVELOPE,
                                                                         EMOJI_EYES))
            await last_message.add_reaction(EMOJI_CHECKMARK)
            await last_message.add_reaction(EMOJI_ENVELOPE)
            await last_message.add_reaction(EMOJI_EYES)

        # display info for user wanting to verify themselves or to message mods.
        elif str(message.content).lower().startswith("$%s verify" % BOT_NAME):
            await message.channel.send(INITIAL_GREETING)

        elif str(message.content).lower().startswith("$%s dm_mods" % BOT_NAME):
            await message.channel.send(HELP_IS_ON_WAY)
            await mod_channel.send(NOTIFICATION_HELP % message.author.id)
            if len(message.content) > len("$%s dm_mods") + 1:  # if user has attached an additional message
                await mod_channel.send("They also sent the following message: \"%s\""
                                       % message.content[len("$%s dm_mods" % BOT_NAME) + 1:])

        elif str(message.content).lower().startswith("$%s" % BOT_NAME) or \
                not str(message.content).lower().startswith("$%s" % BOT_NAME):
            if not str(message.content).lower().startswith("$%s" % BOT_NAME) or len(message.content) > \
                    len("$%s" % BOT_NAME) + 1:
                await message.channel.send(INVALID_COMMAND)
            await message.channel.send(COMMAND_HELP)

    elif message.content.startswith("$%s" % BOT_NAME):  # if users try to call it outside of DMs.
        await message.channel.send("I do not [yet] respond to normal commands outside of DMs :(")


client.run(TOKEN)
