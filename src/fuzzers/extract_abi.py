import json
import subprocess
import sys

def get_contract_abi(file_path, contract_name):
    try:
        command = f"solc --abi {file_path}"
        

        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        abi_start = result.stdout.find(f"{contract_name}")
        if abi_start == -1:
            print(f"Contract {contract_name} not found in {file_path}")
            sys.exit(1)

        abi_start = result.stdout.find('[', abi_start)
            
        open_brackets = 0
        close_brackets = 0

        for i in range(abi_start, len(result.stdout)):
            if result.stdout[i] == '[':
                open_brackets += 1
            elif result.stdout[i] == ']':
                close_brackets += 1

            if open_brackets == close_brackets and open_brackets > 0:
                abi_str = result.stdout[abi_start:i+1]
                break

        print(abi_str)
        abi = json.loads(abi_str)

        return abi

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python script.py <solidity_file_path> <contract_name> <output_file>")
        sys.exit(1)

    solidity_file_path = sys.argv[1]
    contract_name = sys.argv[2]
    output_file = sys.argv[3]

    contract_abi = get_contract_abi(solidity_file_path, contract_name)

    with open(output_file, 'w') as file:
        json.dump(contract_abi, file)

    print(f"ABI for {contract_name} saved to {output_file}")
