# ZUCKERBOT: A simple mod bot for discord 
* Forwards messsages between users' dm and an indicated mod channel
* mods can approve a user's role by reacting with a checkmark 
* User can send images to modbot 
## Commands
### DM ONLY: 
* `$zuck dm_mods` -> user will ask us to message them, it can be related to verification or anything at all 
* `$zuck dm_mods [message from user here]` -> we will receive the alert to contact user + the message they included 
* `$zuck verify` -> will tell the user about verification instructions 
* `[user sends attachment to zuck in chat]` ->zuck interprets this as they're sending screenshot, so the attachment is forwarded here to us in this chat and from that attachment we can react here 
* `$zuck` or `$zuck [anything else]`, bot doesnt understand but lists the available commands
### Anywhere in the server
Mostly disabled for now. If users try to use `$zuck` to tag him, he will say that they can only interact in DMs 
#### Easter egg
`$zuck tell me a joke` can be used anywhere in the server
