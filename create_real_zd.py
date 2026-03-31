#!/usr/bin/env python3
import zipfile
import os
import sys
from pathlib import Path

def create_real_zd(zip_path, zd_path):
    """Create a real .zd file with custom header that can't be extracted as normal zip"""
    
    # Read the original zip file
    with open(zip_path, 'rb') as f:
        zip_data = f.read()
    
    # Create custom .zd format
    zd_data = bytearray()
    
    # Custom magic header (not ZIP compatible)
    zd_data.extend(b'ZD\x01\x00')  # ZD format v1.0
    
    # Add original file size info
    original_size = len(zip_data)
    zd_data.extend(original_size.to_bytes(4, 'little'))
    
    # Simple XOR encryption key
    encryption_key = 0x5A  # 'Z' in hex
    
    # Encrypt the zip data
    encrypted_data = bytearray()
    for byte in zip_data:
        encrypted_data.append(byte ^ encryption_key)
    
    # Add encrypted data
    zd_data.extend(encrypted_data)
    
    # Write the .zd file
    with open(zd_path, 'wb') as f:
        f.write(zd_data)
    
    print(f"✅ Created real .zd file: {zd_path}")
    print(f"Original size: {original_size} bytes")
    print(f"ZD size: {len(zd_data)} bytes")

def extract_real_zd(zd_path, extract_folder):
    """Extract a real .zd file"""
    
    # Read the .zd file
    with open(zd_path, 'rb') as f:
        zd_data = f.read()
    
    # Check magic header
    if not zd_data.startswith(b'ZD\x01\x00'):
        print("❌ Not a valid .zd file!")
        return False
    
    # Get original size
    original_size = int.from_bytes(zd_data[4:8], 'little')
    
    # Decrypt the data
    encrypted_data = zd_data[8:]
    encryption_key = 0x5A
    
    decrypted_data = bytearray()
    for byte in encrypted_data:
        decrypted_data.append(byte ^ encryption_key)
    
    # Create temporary zip file
    temp_zip = "temp_extract.zip"
    with open(temp_zip, 'wb') as f:
        f.write(decrypted_data)
    
    # Extract the zip
    try:
        with zipfile.ZipFile(temp_zip, 'r') as zip_ref:
            zip_ref.extractall(extract_folder)
        
        print(f"✅ Extracted {zd_path} to {extract_folder}")
        
        # Clean up
        os.remove(temp_zip)
        return True
        
    except Exception as e:
        print(f"❌ Error extracting: {e}")
        if os.path.exists(temp_zip):
            os.remove(temp_zip)
        return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage:")
        print("  python create_real_zd.py create input.zip output.zd")
        print("  python create_real_zd.py extract input.zd extract_folder")
        sys.exit(1)
    
    action = sys.argv[1].lower()
    
    if action == "create":
        if len(sys.argv) != 4:
            print("Usage: python create_real_zd.py create input.zip output.zd")
            sys.exit(1)
        
        zip_path = sys.argv[2]
        zd_path = sys.argv[3]
        
        if not os.path.exists(zip_path):
            print(f"❌ File not found: {zip_path}")
            sys.exit(1)
        
        create_real_zd(zip_path, zd_path)
    
    elif action == "extract":
        if len(sys.argv) != 4:
            print("Usage: python create_real_zd.py extract input.zd extract_folder")
            sys.exit(1)
        
        zd_path = sys.argv[2]
        extract_folder = sys.argv[3]
        
        if not os.path.exists(zd_path):
            print(f"❌ File not found: {zd_path}")
            sys.exit(1)
        
        if not os.path.exists(extract_folder):
            os.makedirs(extract_folder)
        
        extract_real_zd(zd_path, extract_folder)
    
    else:
        print("❌ Unknown action. Use 'create' or 'extract'")
        sys.exit(1)
