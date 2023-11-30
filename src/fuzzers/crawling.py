import requests
from bs4 import BeautifulSoup
import sqlite3

class Crawling:
    def __init__(self):
        # url: str = "http://64.110.110.12:5000/users-receiving"
        self.url: str = "http://127.0.0.1:5000/users-receiving"
        self.userid = "capstone" + "123"
        self.addresses = []
        
    def get_address(self) -> list:
        res = requests.post(self.url, data={"userid": self.userid})
        soup = BeautifulSoup(res.text, 'html.parser')
        
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

    def init_database(self):
        self.get_address()
        conn = sqlite3.connect('target_addresses.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contract_addresses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                network TEXT,
                address TEXT,
                ir_fuzz INTEGER DEFAULT 0,
                smartian INTEGER DEFAULT 0,
                ityfuzz INTEGER DEFAULT 0
            )
        ''')

        for address in self.addresses:
            cursor.execute('''
                INSERT INTO contract_addresses (network, address)
                VALUES (?, ?)
            ''', (address["network"], address["address"]))
            
        conn.commit()
        
        conn.close()
        
Crawling().init_database()
