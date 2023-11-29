import requests
import re
from lxml import html
import sqlite3

conn = sqlite3.connect('../databases/contract_addresses.db')
cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE IF NOT EXISTS contract_addresses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        network TEXT,
        address TEXT
    )
''')

# PRAGMA 명령어를 사용하여 "contract_name" 열이 존재하는지 확인
cursor.execute("PRAGMA table_info(contract_addresses)")
columns = cursor.fetchall()
column_names = [column[1] for column in columns]

# "contract_name" 열이 없을 때만 추가
if "contract_name" not in column_names:
    cursor.execute('''
        ALTER TABLE contract_addresses
        ADD COLUMN contract_name TEXT
    ''')
    print("Added 'contract_name' column")
    
conn.commit()



target = ["etherscan.io", "bscscan.com", "arbiscan.io"]

page_urls = [
    f"https://{url}/contractsVerified/{i}?ps=100"  for url in target for i in range(1, 6)
] 
cf_clearance_set = {
                    "etherscan.io" : "",
                    "bscscan.com" : 'kwjpev5x7QLJOOWjzERj6PB9CxyRmYDU_cIBli_7GCs-1698690466-0-1-e7f913a3.5436c44a.2e107480-150.2.1698690466',
                    "polygonscan.com" : 'MAuyhNyryxCCmgx.a85AAoKYwVSsHFXrje3Rcwo0l0Q-1693806663-0-1-e159a75a.8877fc1e.b658f8ba-150.0.0',
                    "ftmscan.com" : 'RndBgvvZ1UIz1nM8pKEoG9DSvjotBeQPIADMQiqakwE-1693806867-0-1-e159a75a.300974a4.b658f8ba-150.0.0',
                    "arbiscan.io" : ""
                    }

pattern = r"https://(.*?)/contractsVerified"
xpath_template = '//*[@id="ContentPlaceHolder1_mainrow"]/div[3]/table/tbody/tr[{}]/td[1]/span/a[1]'
contract_name_template = '//*[@id="ContentPlaceHolder1_mainrow"]/div[3]/table/tbody/tr[{}]/td[2]'




all_data = set()

params = {
    # 'ps': '100',
}

for page_url in page_urls:
    url = re.search(pattern, page_url).group(1)
    # print(url)
    headers = {
        'authority': url,
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'ko-KR,ko;q=0.9,en-US;q=0.8,en;q=0.7',
        'cache-control': 'no-cache',
        # 'cookie': 'cf_chl_2=edfd14a2d84d079; ASP.NET_SessionId=kjpq1f4rdhzhai0zhipke0kx; __cflb=0H28vyb6xVveKGjdV3CYUMgiti5JgVrXJ3a3tvdA5gQ; _ga_PQY6J2Q8EP=GS1.1.1698690464.1.0.1698690464.0.0.0; _ga=GA1.1.811380323.1698690464; bscscan_offset_datetime=+9; cf_clearance=kwjpev5x7QLJOOWjzERj6PB9CxyRmYDU_cIBli_7GCs-1698690466-0-1-e7f913a3.5436c44a.2e107480-150.2.1698690466',
        'pragma': 'no-cache',
        'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
    }
    
    # cf_clearance = cf_clearance_set[url]
    # print(cf_clearance)
    cookies = {
        'cf_chl_2': 'edfd14a2d84d079',
        'ASP.NET_SessionId': 'kjpq1f4rdhzhai0zhipke0kx',
        '__cflb': '0H28vyb6xVveKGjdV3CYUMgiti5JgVrXJ3a3tvdA5gQ',
        '_ga_PQY6J2Q8EP': 'GS1.1.1698690464.1.0.1698690464.0.0.0',
        '_ga': 'GA1.1.811380323.1698690464',
        'bscscan_offset_datetime': '+9',
        'cf_clearance': '3WudC1SF47ycVxxnldrwGM1g615v4SvjIkm0fXAge0A-1698724809-0-1-e7f913a3.5436c44a.2e107480-150.2.1698724809',
    }     
    
    response = requests.get(page_url, headers=headers, cookies=cookies, params=params)
    if response.status_code == 200:
        page_content = html.fromstring(response.content)
        
        # print(page_url)
        for row_number in range(1, 101): 
            
            
            if('arbiscan.io' in page_url): 
                
                xpath_template='//*[@id="transfers"]/div[2]/table/tbody/tr[{}]/td[1]/a'
                xpath_expression = xpath_template.format(row_number)
                data = page_content.xpath(xpath_expression)
                
                contract_name_template2 = '//*[@id="transfers"]/div[2]/table/tbody/tr[{}]/td[2]'
                contract_name_expression = contract_name_template2.format(row_number)
                contract_name = page_content.xpath(contract_name_expression)
                contract_name = contract_name[0].text_content().strip()
            else:  
                xpath_expression = xpath_template.format(row_number)
                data = page_content.xpath(xpath_expression)
                contract_name_expression = contract_name_template.format(row_number)
                contract_name = page_content.xpath(contract_name_expression)
                contract_name = contract_name[0].text_content().strip()
            # print(contract_name)
            if data:
                href = data[0].get("href")
                contract_address = href.split("#code")[0].split("/")[-1]
                all_data.add(contract_address)
                # print(contract_address)
                
                # 중복된 주소를 데이터베이스에서 검색
                cursor.execute("SELECT COUNT(*) FROM contract_addresses WHERE address = ?", (contract_address,))
                count = cursor.fetchone()[0]

                # 중복된 주소가 없는 경우에만 데이터베이스에 삽입
                if count == 0:
                    cursor.execute('''
                        INSERT INTO contract_addresses (network, address, contract_name) VALUES (?, ?, ?)
                    ''', (url, contract_address, contract_name))
                
    else:
        print(page_url)
        print(response.status_code)


conn.commit()
conn.close()


# for item in all_data:
#     print(item)
    
# unique_data = sorted(all_data)

# print(unique_data)
# with open("parsed_data.txt", "a") as file:
#     for item in unique_data:
#         file.write(item + "\n")