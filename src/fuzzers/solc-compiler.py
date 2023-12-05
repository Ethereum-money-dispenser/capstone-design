import subprocess
import sys
import os
import re

def extract_bytecode(solc_output, contract_name):
    contract_start = solc_output.find(f'{contract_name} =======')
    if contract_start == -1:
        print(f"Error: Contract {contract_name} not found in solc output.")
        sys.exit(1)

    binary_start = solc_output.find('Binary:', contract_start)
    if binary_start == -1:
        print(f"Error: Bytecode not found for contract {contract_name}.")
        sys.exit(1)

    bytecode_hex = solc_output[binary_start + len('Binary:'):].strip()

    return bytecode_hex

def save_bytecode_to_file(bytecode_hex, output_file):
    # bytecode_bytes = bytes.fromhex(bytecode_hex)

    with open(output_file, 'w') as file:
        file.write(bytecode_hex)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 save_bytecode.py <input_file.sol> <target_contract>")
        sys.exit(1)

    input_file = sys.argv[1]
    target_contract = sys.argv[2]

    if not input_file.lower().endswith(".sol"):
        print("Error: Input file must have a .sol extension.")
        sys.exit(1)

    output_file = os.path.splitext(input_file)[0]

    solc_command = f'solc {input_file} --bin'
    result = subprocess.run(solc_command, shell=True, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        sys.exit(1)

    bytecode_hex = extract_bytecode(result.stdout, target_contract)

    save_bytecode_to_file(bytecode_hex, output_file + f".bin")
    print(f"Processed bytecode saved to {output_file}.bin")
