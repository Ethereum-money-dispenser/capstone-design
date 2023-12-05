import re
import subprocess
import sys

def set_solc_version(file_path):
    try:
        with open(file_path, 'r') as file:
            solidity_content = file.read()

            pragma_match = re.search(r'pragma solidity (\^?\d+\.\d+\.\d+);', solidity_content)
            
            if pragma_match:
                solidity_version = pragma_match.group(1)

                if solidity_version.startswith('^'):
                    real_version = solidity_version[1:]
                else:
                    real_version = solidity_version

                print(f"Solidity version found in {file_path}: {real_version}")

                command = f"solc-select use {real_version}"
                subprocess.run(command, shell=True)
                print(f"Solidity version set to {real_version}")
            else:
                print("Solidity version not found in pragma statement.")
                sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if len(sys.argv) != 2:
    print("Usage: python3 solc-version.py <file_name>")
    sys.exit(1)

solidity_file_path = sys.argv[1]
set_solc_version(solidity_file_path)
