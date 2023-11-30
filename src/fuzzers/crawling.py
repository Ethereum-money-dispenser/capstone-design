import requests
from bs4 import BeautifulSoup

# url: str = "http://64.110.110.12:5000/users-receiving"
url: str = "http://127.0.0.1:5000/users-receiving"

userid = "capstone" + "123"

def get_address() -> list:
    result = []
    
    res = requests.post(url, data={"userid": userid})
    soup = BeautifulSoup(res.text, 'html.parser')
    table = soup.find('table', attrs={'id':'dataTable'})
    tbody = table.find('tbody')

    for row in tbody.find_all('tr'):
        cols = row.find_all('td')
        network = cols[1].text
        address = cols[2].text
        result.append({
            "network": network, 
            "address": address
        })
        
    return result

