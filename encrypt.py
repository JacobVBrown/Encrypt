#!/usr/bin/env python3
import os
import sys
from Cryptodome.Cipher import AES
from Cryptodome import Random

def encrypt_file(file_path, key=b'this is a 16 key'):
    """
    Encrypts a single file using AES-CFB encryption.
    
    :param file_path: Path to the file to be encrypted.
    :param key:       Encryption key (must be 16, 24, or 32 bytes long).
    """
    # Read the file content in text mode
    with open(file_path, "r", encoding="utf-8") as file_in:
        plaintext = file_in.read()

    # Generate a random IV (initialization vector)
    iv = Random.new().read(AES.block_size)
    
    # Create a new AES cipher object in CFB mode
    cipher = AES.new(key, AES.MODE_CFB, iv)

    # Encrypt the plaintext (encode as bytes first)
    ciphertext = iv + cipher.encrypt(plaintext.encode("utf-8"))

    # Write the ciphertext to a new file with a '.bin' extension
    # Notice we skip the first 16 bytes (which is the IV) when writing
    output_path = file_path + ".bin"
    with open(output_path, "wb") as file_out:
        file_out.write(ciphertext[16:])

    print(f"Encrypted '{file_path}' -> '{output_path}'")

def encrypt_directory(directory_path):
    """
    Recursively walks through a directory and encrypts every file found.
    
    :param directory_path: Path to the directory to be encrypted.
    """
    # Change directory context to the target path
    os.chdir(directory_path)
    
    # Walk through all files in the directory
    for root, _, files in os.walk("."):
        for filename in files:
            file_path = os.path.join(root, filename)
            print(f"Encrypting: {file_path}")
            encrypt_file(file_path)

def main():
    """
    Main entry point. Reads a path from command-line arguments, then
    either encrypts a single file or all files in a directory.
    """
    if len(sys.argv) < 2:
        print("Usage: python encrypt.py [path]")
        sys.exit(1)
    
    path = sys.argv[1]

    # Check what type of path the user provided
    if os.path.isdir(path) and os.path.exists(path):
        encrypt_directory(path)
    elif os.path.isfile(path) and os.path.exists(path):
        encrypt_file(path)
    else:
        print("It's a special file (socket, FIFO, device file), or doesn't exist.")

if __name__ == "__main__":
    main()
