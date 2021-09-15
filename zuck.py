import discord
from discord.ext import commands

################################
description = "A bot that helps approve members for our fb discord"
TOKEN = 'ODg3NDg5MDg3NTYzNDk3NTAy.YUE4nw.jPOZHbaMu-8wXUMOBolwek8A-kw'
# MOD_CHANNEL_ID = 887577242077659146
MOD_CHANNEL_ID = 802794891364270100
# EMOJIS🥶🥶🥶🥶
EMOJI_CHECKMARK = '✅'
EMOJI_ENVELOPE = '✉️'

# discord shtuff
client = discord.Client()
intents = discord.Intents.default()
intents.reactions = True
intents.members = True
bot = commands.Bot(command_prefix='$', description=description, intents=intents)

################################
# MESSAGES #

# Reactions to verify user
verified_message = "Your account has been verified and your access has been granted! Feel free to check " \
                   "any of the verified channels now :-) "
further_verification = "The mod team would like to ask a couple questions about your verification proof. " \
                       "\nDon't worry! A mod will be with you soon.\n\nRemember, you can also dm the mods " \
                       "with `$zuck dm_mods` + the message you want to send! "

# DMing Bot
initial_greeting = """Hello! This is the verifier bot for the FB Interns discord.   

To make things easier for the mods and to accelerate the verification process, **please reply here with a screenshot of 
your career profile that clearly states your full name, as well as the page where it says that you have been accepted to 
a 2022 position.** 

After sending this, a moderator will review this and I will let you know when your access has been approved, 
or if further verification is required. 

If you need further assistance, please type `$zuck dm_mods` so I can send someone your way. You may choose to send a 
custom message to the mods by typing said message right after `$zuck dm_mods`.

The mod team wishes you the best and hopes you have a successful 2022 internship!"""

help_is_on_way = "Help is on the way! Please wait while one of our moderators contacts you. "

proof_received = "Proof received. Mods will review it shortly :)"

command_help = "Commands:  `$zuck verify` to get verification instructions. `$zuck dm_mods` to speak to a mod. You " \
               "may choose to send a custom message to the mods by typing said message right after command " \
               "`$zuck dm_mods`. "

invalid_command = "Beep, boop, I did not get that. "

# Notifying mods about user
notification_verify = "<@%s> has asked for the above image to be used as proof of verification. React with %s to " \
                      "approve the user, or %s to let them know you will be contacting them for further info. "

notification_help = "User <@%s> has asked for a mod to contact them for further discussion.  "


################################

@client.event
async def on_reaction_add(reaction, _user):
    """
    Help mods attribute "verified" role by simply clicking on a react button
    :param reaction: a reaction object to the message. Includes
        - reaction.count , the amount of people having reacted with this emoji
        - reaction.message , the message object within the reaction (see param of on_message for more info)
            - reaction.message.mentions , helping us identify the user tagged in the message, if any
    """
    if reaction.count > 1 and reaction.message.mentions and reaction.message.channel.id == MOD_CHANNEL_ID:
        userino = reaction.message.mentions[0]
        if str(reaction.emoji) == EMOJI_CHECKMARK:
            role = discord.utils.get(reaction.message.guild.roles, name="test_role")
            await userino.add_roles(role)
            await userino.send(verified_message)
        elif str(reaction.emoji) == EMOJI_ENVELOPE:
            await userino.send(further_verification)


@client.event
async def on_message(message):
    """
    The core exchange between zuckerbot and a user
    :param message: the message object sent to the bot. Includes
        - message.channel
        - message.content (the string of a message)
        - message.attachments , a list of attachments such as a picture, a link, etc
        - message.author , the user object that sent the message
    """
    mod_channel = client.get_channel(MOD_CHANNEL_ID)

    if message.author == client.user:
        return
    if message.content.startswith("$zuck tell me a joke"):  # little easter egg
        await message.channel.send("I asked my developers to make a better version of JS. I knew this was a huge "
                                   "thing to ask - but looking back, they did React pretty well!")

    elif isinstance(message.channel, discord.channel.DMChannel):
        # send proof to mod channel, notify mods, and offer reaction options
        if len(message.attachments) != 0:
            await message.channel.send(proof_received)
            await mod_channel.send(message.attachments[0])
            last_message = await mod_channel.send(notification_verify % (message.author.id,
                                                                         EMOJI_CHECKMARK,
                                                                         EMOJI_ENVELOPE))
            await last_message.add_reaction(EMOJI_CHECKMARK)
            await last_message.add_reaction(EMOJI_ENVELOPE)

        # display info for user wanting to verify themselves or to message mods.
        elif str(message.content).lower().startswith("$zuck verify"):
            await message.channel.send(initial_greeting)
        elif str(message.content).lower().startswith("$zuck dm_mods"):
            await message.channel.send(help_is_on_way)
            await mod_channel.send(notification_help % message.author.id)
            if len(message.content) > len("$zuck dm_mods") + 1:  # if user has attached an additional message
                await mod_channel.send("They also sent the following message: \"%s\"" % message.content[
                                                                                        len("$zuck dm_mods") + 1:])
        elif str(message.content).lower().startswith("$zuck") or not str(message.content).lower().startswith("$zuck"):
            if not str(message.content).lower().startswith("$zuck") or len(message.content) > len("$zuck") + 1:
                await message.channel.send(invalid_command)
            await message.channel.send(command_help)

    elif message.content.startswith("$zuck"):  # if users try to call it outside of DMs.
        await message.channel.send("I do not [yet] respond to normal commands outside of DMs :(")

client.run(TOKEN)