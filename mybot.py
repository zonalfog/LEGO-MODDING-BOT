import discord
import asyncio
import sys

# --- HIER DEINE DATEN EINTRAGEN ---
TOKEN = "UR TOKEN" 
# Die ID der KATEGORIE, in der der Bot lesen/schreiben soll
TARGET_CATEGORY_ID = UR CATEROGY  # <--- HIER DEINE NEUE ID EINTRAGEN
# Eine Standard-Kanal-ID, in die deine PowerShell-Antworten gesendet werden sollen
DEFAULT_REPLY_CHANNEL_ID = UR CHANNEL 
# ----------------------------------

intents = discord.Intents.default()
intents.message_content = True 

bot = discord.Client(intents=intents)

async def console_input_loop():
    """Liest deine Eingaben und sendet sie in den Standard-Antwortkanal."""
    await bot.wait_until_ready()
    # Hier lag der Fehler: Der Name muss exakt mit oben übereinstimmen
    channel = bot.get_channel(DEFAULT_REPLY_CHANNEL_ID)
    
    if not channel:
        print(f"\n[FEHLER] Kanal-ID {DEFAULT_REPLY_CHANNEL_ID} nicht gefunden!")
        return

    print(f"\n--- MANUELLER MODUS AKTIV (Kategorie-Modus) ---")
    while not bot.is_closed():
        user_input = await asyncio.to_thread(sys.stdin.readline)
        clean_input = user_input.strip()
        
        if clean_input:
            async with channel.typing():
                await asyncio.sleep(0.5) 
                await channel.send(clean_input)
            print(f"[DU]: {clean_input}")

@bot.event
async def on_ready():
    print(f'Eingeloggt als {bot.user}!')
    bot.loop.create_task(console_input_loop())

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    # Prüfen, ob der Kanal zu der erlaubten Kategorie gehört
    if message.channel.category_id == TARGET_CATEGORY_ID:
        
        print(f"[{message.channel.name}] {message.author.name}: {message.content}")

        content = message.content.lower()

# AUTOMATISCHE ANTWORT: !help
        if content == "!help":
            help_text = """**This is the help list that i created for LEGO-Modding:**

* If you want help with .sf script pls ask @zonalfog
* If you want help with installing mods for LEGO Worlds then pls cut ur downloaded files and paste them in: `C:\\Users\\urname\\AppData\\Roaming\\Warner Bros. Interactive Entertainment\\LEGOWorlds\\SAVEDGAMES\\CONTENT\\CONTENT\\S3-SYSGLOBAL`
* If you want help with the Kestrel Fusion Launcher pls ask Antonie or Doenermann on the Kestrel Fusion Server
* If you want help with modding then pls ask for help on the TTgames Modding server
* If you want help only with modding LCU Then Pls ask Poorer on Kestrel Fusion Launcher Server"""
            
            async with message.channel.typing():
                await asyncio.sleep(1)
                await message.channel.send(help_text)
                await message.channel.send(f"Hey {message.author.mention}!")

# Bot starten
bot.run(TOKEN)
