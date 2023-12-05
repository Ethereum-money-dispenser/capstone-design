import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import sqlite3

db_path = '../databases/contract_addresses.db'

def initialize_database():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(contract_addresses);")
    columns = [column[1] for column in cursor.fetchall()]  # Extract column names
    if 'similar' not in columns:
        cursor.execute("ALTER TABLE contract_addresses ADD COLUMN similar INTEGER DEFAULT 0;")

    conn.commit()
    conn.close()

def update_similar_column(address, similar_value):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("UPDATE contract_addresses SET similar = ? WHERE address = ?;", (similar_value, address))

    conn.commit()
    conn.close()

def select_unprocessed_address():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT address FROM contract_addresses WHERE similar = 0 AND network = 'etherscan.io' LIMIT 1;")
    # cursor.execute("SELECT address FROM contract_addresses WHERE similar = 0 LIMIT 1;")
    result = cursor.fetchone()

    conn.close()

    if result:
        return result[0]
    else:
        return None

def update_similar_addresses(address, similar_value):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("SELECT address FROM contract_addresses WHERE similar = ? ORDER BY id DESC LIMIT 1;", (similar_value,))
    max_id_address = cursor.fetchone()

    if max_id_address:

        cursor.execute("UPDATE contract_addresses SET similar = ? WHERE address = ?;", (similar_value, max_id_address[0],))

        conn.commit()

    conn.close()

def process_etherscan_data(params_base):
    
    cookies = {
    }

    headers = {
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    }
    
    p = 1
    no_matching_entries_str = 'There are no matching entries'

    while True:
        params = params_base.copy()
        params['p'] = str(p)
        address = params['a']
        response = requests.get('https://etherscan.io/find-similar-contracts', params=params, cookies=cookies, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        if no_matching_entries_str in response.text:
            break

        for i in range(1, 100):
            high_value = soup.select_one(f"#ContentPlaceHolder1_tbodyTxnTable > tr:nth-child({i}) > td:nth-child(3)").text
            a_tags = soup.select(f"#ContentPlaceHolder1_tbodyTxnTable > tr:nth-child({i}) > td:nth-child(4) > span > a:nth-child(2)")

            if high_value == "high":
                for a_tag in a_tags:
                    href_value = a_tag.get('href')
                    parsed_url = urlparse(href_value)
                    eth_address = parsed_url.path.split("/")[-1]
                    update_similar_column(eth_address, address)
                    
                    # print(f"Ethereum address: {eth_address}")
            else:
                return

        p += 1



params_base = {
    'a': '0x0cac3d7122dcfbd94b0331213ae7d1ead32295f7',
    'mt': '1',
    'm': 'low',
    'ps': '100',
    'p': '1',
}

def process_all_unprocessed_addresses():
    while True:
        try:    
            initialize_database()
            address = select_unprocessed_address()

            if address is None:
                print("No unprocessed addresses remaining.")
                break

            params_base['a'] = address
            update_similar_column(address, address)
            process_etherscan_data(params_base=params_base)
            update_similar_addresses(address, address)
            print(f"Processed address: {address}")
        except:
            continue

# Example usage
process_all_unprocessed_addresses()