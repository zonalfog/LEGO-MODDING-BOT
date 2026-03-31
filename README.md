# MeinBot - Discord Bot with .zd File Support

A powerful Discord bot with custom .zd file format support, originally created for the LEGO Modding Server.

## Features

### 🗜️ .zd File Format Support
- **Real .zd Format**: Custom encrypted format that cannot be extracted by simple renaming
- **Backward Compatibility**: Supports both old and new .zd formats
- **Smart Detection**: Automatically detects format type

### 📁 File Operations
- **.zip → .zd Conversion**: Convert ZIP files to encrypted .zd format
- **.zd → .zip Conversion**: Convert .zd files back to standard ZIP format
- **.zd Extraction**: Extract all files from .zd archives
- **Drag & Drop Support**: Easy file handling

### 🔒 Security Features
- **XOR Encryption**: Custom encryption with magic header `ZD\x01\x00`
- **Size Verification**: Built-in size validation
- **Secure Temp Files**: Automatic cleanup of temporary files

## Installation

### Requirements
- Python 3.10
- Discord.py library

### Setup
1. Clone this repository
2. Install dependencies:
   ```bash
   pip install discord.py
   ```
3. Configure your bot:
   - Replace `TOKEN` with your Discord bot token
   - Set `TARGET_CATEGORY_ID` to your server category ID
   - Set `DEFAULT_REPLY_CHANNEL_ID` to your default channel ID

### Running the Bot
```bash
python meinbot.py
```

## Usage

### Discord Bot Commands

#### Convert .zip to .zd
```
[Upload a .zip file]
User: make it zd
```
or
```
[Upload a .zip file]
User: .zd
```

#### Extract .zd Files
```
[Upload a .zd file]
User: extract
```

#### Convert .zd to .zip
```
[Upload a .zd file]
User: extract as zip
```

### Standalone Tools

#### Batch Scripts
- `convert_to_zd_interactive.bat` - Interactive .zip to .zd converter
- `extract_zd_interactive.bat` - Interactive .zd extractor
- `create_real_zd.bat` - Create real encrypted .zd files
- `extract_real_zd.bat` - Extract real .zd files

#### Python Tool
```bash
# Create .zd from .zip
python create_real_zd.py create input.zip output.zd

# Extract .zd
python create_real_zd.py extract input.zd extract_folder
```

## .zd File Format

### Structure
```
[4 bytes] Magic Header: "ZD\x01\x00"
[4 bytes] Original file size (little-endian)
[Variable] Encrypted ZIP data (XOR with key 0x5A)
```

### Security
- Custom magic header prevents ZIP extraction
- XOR encryption protects file contents
- Size validation ensures data integrity

## Compatibility

### Supported Formats
- ✅ Real .zd (encrypted)
- ✅ Legacy .zd (renamed ZIP)
- ✅ Standard ZIP files

### Discord Integration
- Works in specified categories only
- Automatic file type detection
- Error handling with user feedback

## Development

### Project Structure
```
meinbot/
├── meinbot.py              # Main bot application
├── create_real_zd.py       # .zd format library
├── convert_to_zd*.bat      # Conversion scripts
├── extract_zd*.bat        # Extraction scripts
└── README.md              # This file
```

### Contributing
Feel free to submit issues and enhancement requests!

## License

This project was originally created for the LEGO Modding Server and is shared for educational purposes.

## Support

For help with:
- **.sf scripts**: Ask @zonalfog
- **LEGO Worlds mods**: Check AppData Roaming path
- **Kestrel Fusion Launcher**: Ask Antonie or Doenermann
- **General modding**: TTgames Modding server
- **LCU modding**: Ask Poorer on Kestrel Fusion Server

---

**Note**: This bot uses a custom .zd format that requires special tools for extraction. Standard ZIP utilities cannot read encrypted .zd files.
