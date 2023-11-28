import sys
from crytic_compile.__main__ import main
import sqlite3

args = sys.argv[1:]

if len(args) < 1 or '-h' in args or '--help' in args:
    print('Usage: python3 downloaer.py [-d | --address <contract_address>]')
    print('                            [-a | --all]')
    print('                            [-p | --path <path_to_contracts>]')
    print('                            [-f | --file <path_to__contract_file>]]')
    print('                            [-h | --help]')
    print('')
    print('Options:')
    print('  -h, --help                         Show this help message and exit')
    print('  -d, --address <contract_address>   Download a contract with the given address')
    print('  -a, --all                          Download all contracts in database')
    print('  -p, --path <path_to_contracts>     Download contracts to the given path')
    print('  -f, --file <path_to_contract_file> Download a contract from the given file')
    sys.exit(1)
    
path_arg = ['--export-dir', '.']
    
if '-p' in args or '--path' in args:
    index = args.index('-p') if '-p' in args else args.index('--path')
    path_arg[1] = args[index + 1]
    print('Downloading contracts to the given path: ' + path_arg[1])
    
def download_contract(contract_address: str):
    sys.argv = ['', contract_address] + path_arg
    main()

def download_all_contracts():
    conn = sqlite3.connect('../crawling/contract_addresses.db')
    conn.row_factory = sqlite3.Row
    
    cursor = conn.cursor()
    cursor.execute('SELECT address FROM contract_addresses')
    rows = cursor.fetchall()
    
    conn.close()
    
    for row in rows: download_contract(row['address'])
    
if '-a' in args or '--all' in args:
    print('Downloading all contracts in database')
    download_all_contracts()
    
if '-d' in args or '--address' in args:
    index = args.index('-d') if '-d' in args else args.index('--address')
    contract_address = args[index + 1]
    print('Downloading a contract with address: ' + contract_address)
    download_contract(contract_address)

if '-f' in args or '--file' in args:
    index = args.index('-f') if '-f' in args else args.index('--file')
    file_path = args[index + 1]
    print('Downloading a contract from the given file: ' + file_path)
    
    with open(file_path, 'r') as f:
        while True:
            contract_address = f.readline().strip()
            if not contract_address:
                break
            download_contract(contract_address)
