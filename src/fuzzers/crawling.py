import requests
from bs4 import BeautifulSoup

url:str = "http://64.110.110.12:5000/"
url:str = "http://127.0.0.1:5000/"

def get_address() -> list:
    