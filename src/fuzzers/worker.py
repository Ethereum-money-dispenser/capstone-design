# Managing fuzzers
import sqlite3
import os
import threading
import subprocess
import json
import requests
from bs4 import BeautifulSoup
# from downloader import Downloader
from subprocess import CompletedProcess
from sqlite3 import Connection, Cursor
from requests import Response

class Fuzzer():
    def __init__(self, id) -> None:
        self.id = id
        self.addresses: list = []
        self.etherscan_api_key: str = "9NFWVRRXYWJI1BUU3H8Y9IZTZKXGF4TUK3"
        self.bscscan_api_key: str = "[Bscscan API key]"
        self.arbiscan_api_key: str = "[Arbiscan API key]"
        # self.url_sending: str = "http://64.110.110.12:5000/users-sending"
        # self.url_receiving: str = "http://64.110.110.12:5000/users-receiving"
        self.url_sending: str = "http://127.0.0.1:5000/users-sending"
        self.url_receiving: str = "http://127.0.0.1:5000/users-receiving"
        self.etherscan_api_link: str = "https://api.etherscan.io/api"
        self.bscscan_api_link: str = "https://api.bscscan.com/api"
        self.arbiscan_api_link: str = "https://api.arbiscan.io/api"

    def load_dataset(self):
        '''
        Load the dataset from server
        '''
        
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'http://127.0.0.1:5000',
            'Pragma': 'no-cache',
            'Referer': 'http://127.0.0.1:5000/users-receiving',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }
        
        data = {
            'userid': self.id,
        }

        res: Response = requests.post(self.url_receiving, data=data, headers=headers)
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
        get_sourcecode_query: str = f"&action=getsourcecode&address={address}&apikey={self.etherscan_api_key}"
        
        if network == "etherscan.io":
            get_abi: str = self.etherscan_api_link + get_abi_query
            get_sourcecode: str = self.etherscan_api_link + get_sourcecode_query
        elif network == "bscscan.com":
            get_abi: str = self.bscscan_api_link + get_abi_query
            get_sourcecode: str = self.bscscan_api_link + get_sourcecode_query
        elif network == "arbiscan.io":
            get_abi: str = self.arbiscan_api_link + get_abi_query
            get_sourcecode: str = self.arbiscan_api_link + get_sourcecode_query
        
        abi_params = {
            "module": "contract",
            "action": "getabi",
            "address": address,
            "apikey": self.etherscan_api_key
        }
        abi_response = requests.get(self.etherscan_api_link, params=abi_params)
        abi_result = abi_response.json()

        abi = abi_result["result"]
        
        byte_params = {
            "module": "proxy",
            "action": "eth_getCode",
            "address": address,
            "apikey": self.etherscan_api_key
        }
        
        byte_response = requests.get(self.etherscan_api_link, params=byte_params)
        byte_result = byte_response.json()
        bytecode = byte_result["result"]
        
        return {"abi" : abi, "bytecode": bytecode}
        
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

# example        
fuzz = Fuzzer('capstone122')
fuzz.load_dataset()
target_dict = fuzz.get_information_from_address(fuzz.addresses[0]['address'],fuzz.addresses[0]['network'])
print(target_dict)