import discord
import asyncio
import sys
import zipfile
import io
import os
import shutil
import tempfile

# --- HERE UR DATA ---
TOKEN = "YOUR TOKEN" 
# Die ID der KATEGORIE, in der der Bot lesen/schreiben soll
TARGET_CATEGORY_ID = YOUR CATEROGY  # <--- HIER DEINE NEUE ID EINTRAGEN
# Eine Standard-Kanal-ID, in die deine PowerShell-Antworten gesendet werden sollen
DEFAULT_REPLY_CHANNEL_ID = YOUR CHANNEL 
# ----------------------------------

intents = discord.Intents.default()
intents.message_content = True 

bot = discord.Client(intents=intents)

# Real .zd format functions
def create_real_zd(zip_data):
    """Create a real .zd file with custom encryption from zip data"""
    zd_data = bytearray()
    
    # Custom magic header
    zd_data.extend(b'ZD\x01\x00')
    
    # Add original file size info
    original_size = len(zip_data)
    zd_data.extend(original_size.to_bytes(4, 'little'))
    
    # Simple XOR encryption
    encryption_key = 0x5A
    encrypted_data = bytearray()
    for byte in zip_data:
        encrypted_data.append(byte ^ encryption_key)
    
    # Add encrypted data
    zd_data.extend(encrypted_data)
    
    return bytes(zd_data)

def extract_real_zd(zd_data):
    """Extract real .zd file data"""
    # Check magic header
    if not zd_data.startswith(b'ZD\x01\x00'):
        return None, "Not a valid real .zd file"
    
    try:
        # Get original size
        original_size = int.from_bytes(zd_data[4:8], 'little')
        
        # Decrypt the data
        encrypted_data = zd_data[8:]
        encryption_key = 0x5A
        
        decrypted_data = bytearray()
        for byte in encrypted_data:
            decrypted_data.append(byte ^ encryption_key)
        
        return bytes(decrypted_data), None
    except Exception as e:
        return None, f"Error decrypting .zd file: {str(e)}"

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

        # Check for file attachments
        if message.attachments:
            for attachment in message.attachments:
                filename = attachment.filename.lower()
                
                # Handle .zd file extraction
                if filename.endswith('.zd') and 'extract' in content:
                    try:
                        # Download the .zd file
                        file_data = await attachment.read()
                        
                        # Check if user wants to convert to .zip
                        if 'as zip' in content:
                            # Try to extract as real .zd format first
                            decrypted_data, error = extract_real_zd(file_data)
                            
                            if error is None:
                                # Real .zd format - convert to .zip
                                zip_filename = attachment.filename.replace('.zd', '.zip')
                                await message.channel.send(f"Converted REAL .zd to .zip:", 
                                                          file=discord.File(io.BytesIO(decrypted_data), zip_filename))
                                await message.channel.send(f"✅ Successfully converted REAL .zd to {zip_filename}")
                            else:
                                # Try old format - just rename
                                zip_filename = attachment.filename.replace('.zd', '.zip')
                                await message.channel.send(f"Converted old .zd to .zip:", 
                                                          file=discord.File(io.BytesIO(file_data), zip_filename))
                                await message.channel.send(f"✅ Successfully converted old .zd to {zip_filename}")
                        else:
                            # Normal extraction
                            # Try to extract as real .zd format first
                            decrypted_data, error = extract_real_zd(file_data)
                            
                            if error is None:
                                # Real .zd format - extract decrypted data
                                with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as temp_zip:
                                    temp_zip.write(decrypted_data)
                                    temp_zip_path = temp_zip.name
                                
                                try:
                                    with zipfile.ZipFile(temp_zip_path, 'r') as zip_ref:
                                        extracted_files = zip_ref.namelist()
                                        
                                        # Create temp directory
                                        temp_dir = f"temp_extract_{message.id}"
                                        os.makedirs(temp_dir, exist_ok=True)
                                        zip_ref.extractall(temp_dir)
                                    
                                    # Send extracted files back
                                    files_sent = []
                                    for extracted_file in extracted_files:
                                        file_path = os.path.join(temp_dir, extracted_file)
                                        if os.path.isfile(file_path):
                                            await message.channel.send(f"Extracted: {extracted_file}", 
                                                                      file=discord.File(file_path, extracted_file))
                                            files_sent.append(extracted_file)
                                    
                                    # Cleanup
                                    shutil.rmtree(temp_dir)
                                    
                                    await message.channel.send(f"✅ Successfully extracted REAL .zd format: {len(files_sent)} files")
                                    
                                finally:
                                    os.unlink(temp_zip_path)
                                    
                            else:
                                # Try old format (treat as regular zip)
                                try:
                                    temp_dir = f"temp_extract_{message.id}"
                                    os.makedirs(temp_dir, exist_ok=True)
                                    
                                    zd_path = os.path.join(temp_dir, attachment.filename)
                                    with open(zd_path, 'wb') as f:
                                        f.write(file_data)
                                    
                                    with zipfile.ZipFile(zd_path, 'r') as zip_ref:
                                        extracted_files = zip_ref.namelist()
                                        zip_ref.extractall(temp_dir)
                                    
                                    # Send extracted files back
                                    files_sent = []
                                    for extracted_file in extracted_files:
                                        file_path = os.path.join(temp_dir, extracted_file)
                                        if os.path.isfile(file_path):
                                            await message.channel.send(f"Extracted: {extracted_file}", 
                                                                      file=discord.File(file_path, extracted_file))
                                            files_sent.append(extracted_file)
                                    
                                    # Cleanup
                                    shutil.rmtree(temp_dir)
                                    
                                    await message.channel.send(f"✅ Extracted old .zd format: {len(files_sent)} files")
                                    
                                except Exception as old_error:
                                    await message.channel.send(f"❌ Not a valid .zd file. Neither real nor old format supported.")
                        
                    except Exception as e:
                        await message.channel.send(f"❌ Error processing .zd file: {str(e)}")
                
                # Handle .zip to .zd conversion
                elif filename.endswith('.zip') and ('zd' in content or '.zd' in content):
                    try:
                        # Download the .zip file
                        file_data = await attachment.read()
                        
                        # Create REAL .zd file with encryption
                        zd_data = create_real_zd(file_data)
                        zd_filename = attachment.filename.replace('.zip', '.zd')
                        
                        # Send as REAL .zd file
                        await message.channel.send(f"Created REAL encrypted .zd:", 
                                                  file=discord.File(io.BytesIO(zd_data), zd_filename))
                        
                        await message.channel.send(f"✅ Successfully converted {attachment.filename} to REAL .zd format")
                        await message.channel.send("🔒 This .zd file uses custom encryption and cannot be extracted by renaming!")
                        
                    except Exception as e:
                        await message.channel.send(f"❌ Error converting to .zd file: {str(e)}")

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