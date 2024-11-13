import os
from twitchio.ext import commands
from mcpi.minecraft import Minecraft
from mcrcon import MCRcon
import random

BOT_TOKEN = "" # OAuth token
CLIENT_ID = "" # Twitch client ID
CLIENT_SECRET = "" # Twitch client secret
CHANNEL_NAME = "" # Twitch channel name

mc = Minecraft.create("localhost", 4711)
mcr = MCRcon("YOUR IP HERE", "YOUR PASSWORD HERE") # minecraft server IP and password (Rcon needs to be enabled)

mcr.connect()

mob_ids = {
    "zumbi": 54,
    "esqueleto": 34,
    "creeper": 50,
    "aranha": 52,
    "bruxa": 66,
    "enderman": 58,
    "slime": 55,
    "ghast": 56,
    "blaze": 61,
    "cavalo_esqueleto": 28,
    "cavalo_zumbi": 27,
    "zumbi_vagante": 134,
    "vindicador": 126,
    "invocador": 125,
    "panda": 105,
    "lhama": 103,
    "coelho": 101,
    "raposa": 122,
    "morcego": 65,
    "baiacu": 90,
    "guardião": 68,
    "guardião_ancião": 69,
    "shulker": 61,
    "cubomagma": 62,
    "tartaruga": 93,
    "urso_polar": 102,
    "vendedor_ambulante": 126,
    "strider": 111,
    "piglin": 113,
    "hoglin": 114,
    "zoglin": 122
}

bot = commands.Bot(
    token=BOT_TOKEN,
    client_id=CLIENT_ID,
    nick="YOUR NICK", # bot nickname is the same as your Twitch username
    prefix="!",
    initial_channels=[CHANNEL_NAME]
)
def spawn_mob(mob_id, x, y, z):
    x = int(round(x))
    y = int(round(y))
    z = int(round(z))
    mc.spawnEntity(x, y, z, mob_id)
    mc.postToChat(f"Spawned a {mob_id} at ({x}, {y}, {z})!")

# Evento de inicialização
@bot.event
async def event_ready():
    print(f"Bot {bot.nick} conected and ready!")


# Evento de mensagem no chat
@bot.event
async def event_message(message):
    if message.author.name.lower() == bot.nick.lower():
        return

    print(f"Message from {message.author.name}: {message.content}")
    
    # Caso de uso de bits para as ações

    # # Verificar se a mensagem contém bits (cheers)
    # if message.bits >=50:
    #     print(f"Recebido um cheer de {message.bits} bits de {message.author.name}!")
        
    #     # Coloca um bloco aleatório no Minecraft
    #     bloco_id = random.randint(0, 455)  # Faixa de IDs de blocos aleatórios (exemplo entre 455 e 500)
    #     print(f"Colocando bloco de ID {bloco_id} no Minecraft...")
    #     player_pos = mc.player.getTilePos()  # Posição do jogador no Minecraft
    #     mc.setBlock(player_pos.x, player_pos.y, player_pos.z, bloco_id)  # Coloca o bloco na posição do jogador
    
    # if message.bits >= 100:
    #     print(f"Recebido um cheer de {message.bits} bits de {message.author.name}!")
        
    #     mcr.command('execute as @a[limit=500] run summon minecraft:lightning_bolt')
    #     await message.channel.send(f"Obrigado pela doação de {message.bits} bits, {message.author.name}! Chuva de 500 lightning_bolt!")
        

    # if message.bits >= 300:
    #     print(f"Recebido um cheer de {message.bits} bits de {message.author.name}!")

    #     x = random.randint(-200, 200)
    #     y = random.randint(-200, 200)
    #     z = random.randint(-200, 200)
    #     print(f"Teletransportando para {x}, {y}, {z}...")

    #     mc.player.setTilePos(x, y, z)

    #     await message.channel.send(f"Obrigado pela doação de {message.bits} bits, {message.author.name}! teleport para {x}, {y}, {z}!")


    # if message.bits >= 500:
    #     print(f"Recebido um cheer de {message.bits} bits de {message.author.name}!")
    #     player_pos = mc.player.getTilePos()
    #     mc.spawnEntity(player_pos.x + 1, player_pos.y, player_pos.z, "minecraft:zombie")
    #     await message.channel.send(f"Obrigado pela doação de {message.bits} bits, {message.author.name}! Um zombie foi gerado!")
    # # Processa outros comandos
    # await bot.handle_commands(message)

    # if message.bits >= 1000:
    #     print(f"Recebido um cheer de {message.bits} bits de {message.author.name}!")
    #     mcr.command('summon minecraft:wither')
    #     await message.channel.send(f"Obrigado pela doação de {message.bits} bits, {message.author.name}! Um wither foi gerado!")

# Comando 'oi' no chat da Twitch
@bot.command(name='hello')
async def hello(ctx):
    await ctx.send(f'Hello, {ctx.author.name}!')

@bot.command(name='spawnmob')
async def spawnmob(ctx, mob_name: str):
    if mob_name not in mob_ids:
        await ctx.send(f"Mob {mob_name} is invalid! Use one of the following: {', '.join(mob_ids.keys())}")
        return

    players = mc.getPlayerEntityIds()
    if not players:
        await ctx.send("No players are online to get the position.")
        return

    random_player = random.choice(players)
    player_pos = mc.entity.getPos(random_player)
    x = player_pos.x + random.randint(-5, 5)
    y = player_pos.y
    z = player_pos.z + random.randint(-5, 5)
    spawn_mob(mob_ids[mob_name], x, y, z)
    await ctx.send(f"Spawning a {mob_name} at ({x}, {y}, {z}) next to {random_player}!")


@bot.command(name='timeset')
async def timeset(ctx, timeset: str = "day"):
    if timeset == "day":
        mcr.command('time set day')
    if timeset == "night":
        mcr.command('time set night')
    if timeset == "midnight":
        mcr.command('time set midnight')
    if timeset == "evening":
        mcr.command('time set noon')

@bot.command(name='weather')
async def weather(weather):
    if weather == "sun":
        resp = mcr.command('weather clear')
        print(resp)
    if weather == "rain":
        resp = mcr.command('weather rain')
        print(resp)
    if weather == "storm":
        resp = mcr.command('weather thunder')
        print(resp)

@bot.command(name='trident')
async def trident(ctx):
    resp = mcr.command("execute as @a[limit=50] run summon minecraft:trident ~ 200 ~")
    print(resp)
    await ctx.send(f"{ctx.author.name}, raining tridents!")


@bot.command(name='arena')
async def arena(ctx):
    # Pega os jogadores online no servidor
    players = mc.getPlayerEntityIds()
    if not players:
        await ctx.send("No players online to create the arena.")
        return

    random_player = random.choice(players)
    player_pos = mc.entity.getPos(random_player)

    player_pos.y = int(player_pos.y)

    ground_y = player_pos.y - 1  

    radius = 10 

    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            if dx**2 + dz**2 <= radius**2: 
                mc.setBlock(player_pos.x + dx, ground_y, player_pos.z + dz, 2) 

    for dx in range(-radius - 1, radius + 2):
        for dy in range(0, radius + 3):  
            for dz in range(-radius - 1, radius + 2):
                if dx**2 + dz**2 <= (radius + 1)**2 and dx**2 + dz**2 > radius**2:  
                    mc.setBlock(player_pos.x + dx, ground_y + dy, player_pos.z + dz, 1)  

    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            if (dx == radius or dz == radius or dx == -radius or dz == -radius) and dx**2 + dz**2 <= (radius + 1)**2:
                for y in range(ground_y, ground_y + radius + 2):  
                    mc.setBlock(player_pos.x + dx, y, player_pos.z + dz, 17)  

    for dx in range(-radius, radius + 1):
        for dz in range(-radius, radius + 1):
            if dx**2 + dz**2 <= radius**2:
                mc.setBlock(player_pos.x + dx, ground_y + radius, player_pos.z + dz, 20)  

    for dx in range(-radius + 1, radius):
        for dy in range(1, radius):
            for dz in range(-radius + 1, radius):
                if dx**2 + dz**2 <= radius**2:
                    mc.setBlock(player_pos.x + dx, ground_y + dy, player_pos.z + dz, 0) 

    num_lava_pools = random.randint(3, 5)  
    for _ in range(num_lava_pools):
        x = player_pos.x + random.randint(-radius + 1, radius - 1)
        z = player_pos.z + random.randint(-radius + 1, radius - 1)

        if x**2 + z**2 <= radius**2:
            for dx in range(-1, 2):  
                for dz in range(-1, 2):  
                    if x + dx**2 + z + dz**2 <= radius**2:
                        mc.setBlock(x + dx, ground_y, z + dz, 10) 

    hostile_mobs = [
        50,  # Creeper
        51,  # Skeleton
        52,  # Spider
        54,  # Zombie
        5,   # Wither Skeleton (substituindo Slime)
        6,   # Stray (substituindo Ghast)
        58,  # Enderman
        61,  # Blaze
        64,  # Wither
        23,  # Husk
        37,  # Illusioner (substituindo Magma Cube)
        36   # Vindicator (substituindo Zombie Villager)
    ]


    for _ in range(3): 
        mob_id = random.choice(hostile_mobs)

        x = int(player_pos.x + random.randint(-radius + 2, radius - 2))
        y = int(ground_y + 1)  
        z = int(player_pos.z + random.randint(-radius + 2, radius - 2))

        try:
            mc.spawnEntity(x, y, z, mob_id)
            mc.postToChat(f"Hostile mob {mob_id} spawned at ({x}, {y}, {z}) inside the arena!")
        except Exception as e:
            mc.postToChat(f"Error to spawn mob: {e}")

    mc.postToChat(f"Arena created around {random_player} and three hostile mobs spawned!")
    await ctx.send(f"Arena created around {random_player}!")

@bot.command(name='random_effect')
async def random_effect(ctx):
    players = mc.getPlayerEntityIds()
    if not players:
        await ctx.send("No players online to apply the effect.")
        return

    random_player = random.choice(players)
    troll_actions = ["teleport", "fall", "prison"]
    action = random.choice(troll_actions)

    if action == "teleport":
        x = random.randint(-20, 20)
        y = random.randint(5, 10)
        z = random.randint(-20, 20)
        mc.entity.setPos(random_player, x, y, z)
        mc.postToChat(f"Player {random_player} was teleported!")
        await ctx.send(f"Applyed a teleport effect to {random_player}.")

    elif action == "fall":
        pos = mc.entity.getPos(random_player)
        mc.entity.setPos(random_player, pos.x, pos.y + 50, pos.z)
        mc.postToChat(f"Player {random_player} was sent to the sky!")
        await ctx.send(f"Applyed a fall effect to Player {random_player}.")

    elif action == "prison":
        pos = mc.entity.getPos(random_player)
        for dx in range(-2, 3):
            for dy in range(-1, 4):
                for dz in range(-2, 3):
                    if dx in (-2, 2) or dy in (-1, 3) or dz in (-2, 2):
                        mc.setBlock(pos.x + dx, pos.y + dy, pos.z + dz, 49)

        mc.postToChat(f"Player {random_player} was sent to prison!")
        await ctx.send(f"Applyed a prison effect to {random_player}.")


@bot.command(name='thunder')
async def thunder(ctx):
    resp = mcr.command('execute as @p[limit=5000] run summon minecraft:lightning_bolt')
    print(resp)
    await ctx.send('Thunders sent!')


@bot.command(name='help')
async def help_command(ctx):
    await ctx.send("Available commands:")
    await ctx.send("!spawnmob <nome_do_mob> - spawn a mob around a player.")
    await ctx.send("example: !spawnmob zombie")
    await ctx.send("!random_effect - apply a random troll effect to a player.")
    await ctx.send("!arena - create an arena around a player randomly, with walls of stone, glass, lava and mobs.")
    await ctx.send("!thunder - send thunder to all online players.")
    await ctx.send("!timeset <day|night|midnight|evening> - Change the game time.")
    await ctx.send("!weather <rain|sun|storm> - change the weather.")
    await ctx.send("!trident - send tridents to all online players.")

# Inicia o bot
if __name__ == "__main__":
    try:
        bot.run()

    finally:
        mcr.disconnect()