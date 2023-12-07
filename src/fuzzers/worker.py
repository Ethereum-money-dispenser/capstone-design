# Managing fuzzers
import sqlite3
import os
import threading
import subprocess
import json
import requests
from bs4 import BeautifulSoup
from downloader import Downloader
from subprocess import CompletedProcess
from sqlite3 import Connection, Cursor
from requests import Response

class Fuzzer():
    def __init__(self) -> None:
        self.addresses: list = []
        self.etherscan_api_key: str = "[Etherscan API key]"
        self.bscscan_api_key: str = "[Bscscan API key]"
        self.arbiscan_api_key: str = "[Arbiscan API key]"
        # self.url_sending: str = "http://64.110.110.12:5000/users-sending"
        # self.url_receiving: str = "http://64.110.110.12:5000/users-receiving"
        self.url_sending: str = "http://127.0.0.1:5000/users-sending"
        self.url_receiving: str = "http://127.0.0.1:5000/users-receiving"
        self.etherscan_api_link: str = "https://api.etherscan.io/api?module=contract"
        self.bscscan_api_link: str = "https://api.bscscan.com/api?module=contract"
        self.arbiscan_api_link: str = "https://api.arbiscan.io/api?module=contract"
    
    def load_dataset(self):
        '''
        Load the dataset from server
        '''
        res: Response = requests.get(self.url_receiving)
        soup: BeautifulSoup = BeautifulSoup(res.text, 'html.parser')
        
        table = soup.find('table', attrs={'id':'dataTable'})
        tbody = table.find('tbody')
        
        for row in tbody.find_all('tr'):
            cols = row.find_all('td')
            network = cols[1].text
            address = cols[2].text
            self.addresses.append({
                "network": network, 
                "address": address
            })
    
    def get_information_from_address(self, address: str, network: str) -> None:
        # get contract abi, source code, bytecode from address and save to the file
        get_abi_query: str = f"&action=getabi&address={address}"
        get_sourcecode_query: str = f"&action=getsourcecode&address={address}&apikey{self.etherscan_api}"
        
        if network == "etherscan":
            get_abi: str = self.etherscan_api_link + get_abi_query + f"&apikey{self.etherscan_api}"
            get_sourcecode: str = self.etherscan_api_link + get_sourcecode_query + f"&apikey{self.etherscan_api}"
        elif network == "bscscan":
            get_abi: str = self.bscscan_api_link + get_abi_query + f"&apikey{self.bscscan_api}"
            get_sourcecode: str = self.bscscan_api_link + get_sourcecode_query + f"&apikey{self.bscscan_api}"
        elif network == "arbiscan":
            get_abi: str = self.arbiscan_api_link + get_abi_query + f"&apikey{self.arbiscan_api}"
            get_sourcecode: str = self.arbiscan_api_link + get_sourcecode_query + f"&apikey{self.arbiscan_api}"
        
        source_code: str = json.loads(requests.get(get_abi).text)['result'][0]['SourceCode']
        
    def manage_fuzzer(self):
        pass
        
    def run_command(self, command: str, timeout: int = 60):
        process: CompletedProcess = subprocess.run(command, capture_output=True, text=True, timeout=timeout)

class IR_fuzzer(Fuzzer):
    def __init__(self) -> None:
        super().__init__()
        
    def manage_fuzzer(self):
        super().manage_fuzzer()
        
        for address in self.addresses:
            os.system(f"python3 downloader.py -d {address['address']} -f .")

class Smartian_fuzzer(Fuzzer):
    def __init__(self) -> None:
        super().__init__()
        pass
        
    def manage_fuzzer(self):
        super().manage_fuzzer()
        
        os.chdir("Smartian")

        command: str = f"dotnet build/Smartian.dll fuzz -p {bytecode_file} -a {abi_file} -t {time_limit} -o {output_dir}"

class ity_fuzzer(Fuzzer):
    def __init__(self) -> None:
        super().__init__()
        pass
        
    def manage_fuzzer(self) -> None:
        super().manage_fuzzer()
        
        for address in self.addresses:
            # check the version of the contract
            
            command: str = f"ityfuzz evm -t {address['address']} -c ETH"
            if address['network'] == "etherscan.io": 
                command += f"--onchain-etherscan-api-key {self.etherscan_api}"
                
            self.run_command(command, 3600)
         
