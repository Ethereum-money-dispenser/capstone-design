# Managing fuzzers
import sqlite3
import os
import sys
import threading
import subprocess
import json
import requests
from bs4 import BeautifulSoup
from bs4 import Tag
# from downloader import Downloader
from subprocess import CompletedProcess
from sqlite3 import Connection, Cursor
from requests import Response

from typing import Dict, List


class slither():
    def __init__(self):
        self.etherscan_api_key = "U3ENG8WJRUVZAYN4AR72JPQUVB7T75VNJA"
        self.bscan_api_key = "YDTDBABWBTE4SJSVPX67BE7XN4553KCHKM"
        self.arbiscan_api_key = "3GVP26N8DRRIMZ2DFWSGIIUJCIAKAGB85D"

    
    def load_dataset(self) -> List[Dict[str, str]]:
        '''
        Load the dataset from server
        '''
        # SQLite 데이터베이스 연결
        conn = sqlite3.connect('../databases/contract_addresses.db')
        cursor = conn.cursor()

        # 모든 데이터를 선택하는 SQL 쿼리 실행
        cursor.execute("SELECT * FROM contract_addresses")

        # 결과 가져오기
        rows = cursor.fetchall()

        addresses = []

        # 결과 출력
        for row in rows:
            addresses.append({'network': row[1], 'address': row[2]})

        # 데이터베이스 연결 종료
        conn.close()

        return addresses

            
    

    def manage_slither(self, data: Dict[str, str]):
        target = ["etherscan.io", "bscscan.com", "arbiscan.io"]
        
        if data['network'] == "etherscan.io":
            command: str = f"slither {data['address']} --exclude-optimization --exclude-informational --exclude-low --exclude-medium --etherscan-apikey f{self.etherscan_api_key}" 
            
        if data['network'] == "bscscan.com":
            command: str = f"slither bsc:{data['address']} --exclude-optimization --exclude-informational --exclude-low --exclude-medium --bsscan-apikey f{self.bscan_api_key}" 

        if data['network'] == "arbiscan.io":
            command: str = f"slither arbi:{data['address']} --exclude-optimization --exclude-informational --exclude-low --exclude-medium --arbiscan-apikey f{self.arbiscan_api_key}" 

        command += f" 2>> result/{data['address']}"

        process: CompletedProcess = subprocess.run(command.split(), capture_output=True, text=True, cwd="")



sli = slither()
dataset = sli.load_dataset()
print(dataset[0])
for data in dataset:
    sli.manage_slihter(data)
