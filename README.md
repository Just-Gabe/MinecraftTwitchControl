# MinecraftTwitchControl
An easy to use tool that enables chat control over a minecraft server.

All you have to do is configure your credentials in

```
BOT_TOKEN = "" # OAuth token
CLIENT_ID = "" # Twitch client ID
CLIENT_SECRET = "" # Twitch client secret
CHANNEL_NAME = "" # Twitch channel name

mc = Minecraft.create("localhost", 4711)
mcr = MCRcon("YOUR IP HERE", "YOUR PASSWORD HERE") # minecraft server IP and password (Rcon needs to be enabled)
```

And

```
bot = commands.Bot(
    token=BOT_TOKEN,
    client_id=CLIENT_ID,
    nick="YOUR NICK", # bot nickname is the same as your Twitch username
    prefix="!",
    initial_channels=[CHANNEL_NAME]
```

Viewers on chat will be able to interact via bot commands:


Available commands:
"!spawnmob <nome_do_mob> - spawn a mob around a player."
"example: !spawnmob zombie"
"!random_effect - apply a random troll effect to a player."
"!arena - create an arena around a player randomly, with walls of stone, glass, lava and mobs."
"!thunder - send thunder to all online players."
"!timeset <day|night|midnight|evening> - Change the game time."
"!weather <rain|sun|storm> - change the weather."
"!trident - send tridents to all online players."
