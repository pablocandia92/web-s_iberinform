import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup as bs
import requests
from lxml import html, etree
import time


BASE_URL = 'https://www.iberinform.es'
def open_browser():
    path = os.path.abspath('linux64/chromedriver')
    url= "https://www.iberinform.es/busquedaEmpresa?csrf=C4kAbBLl0k63DekQczGJ-OTAEnmgJFglNODVAsyXHPc%3AAAABi0yJ2dY%3AyuPdFygEd-6rrM3iwI8FdA&criterioBusqueda=viveros"

    options = Options()
    options.add_argument('--incognito')
    options.add_argument('start-maximized')
    service = Service(path)
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(url)
    data = []
    html = driver.page_source
    soup = bs(html, features='html.parser')
    driver.quit()

    return(soup)

def extract_data(soup):
    table = soup.find('table', class_="table table-striped resultados__tabla")
    #NOMBRES DE COLUMNAS
    names_col_3 = table.find('thead')
    list_col_3 = [th.text for th in names_col_3.find_all('th')]
    #VALORES
    data = []
    container_body_table = table.find('tbody')
    list_all_companies = container_body_table.find_all('tr')
    for i in range(0, len(list_all_companies)):
        company = list_all_companies[i].find_all('td')
        company_url = (company[0].find('a')).get('href')
        company_nombre = (company[0].text).strip()
        company_provincia = company[1].text
        company_municipio = company[2].text
        data.append([company_nombre, company_provincia, company_municipio, company_url])
        
        break
    return data, company_url

def extract_data_by_company(url):
    company_url = BASE_URL + url
    test_url = url
    
    REQUEST_HEADER = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-GB,en;q=0.5",
        "Connection": "keep-alive",
        "Cookie": "RETURNING_VISITOR=; csrf=tvYseSzrva4zifbZRQkwK8DccZ2zNsbZuo5gBhsODVI:AAABi1Sl0kQ:kcB3yL6J5RcQCKIn8cSZ0A; cookieconsent_status=necesarias|preferencias|estadisticas|marketing; visitor_id210552=784211688; visitor_id210552-hash=df3a9a1b872768e963d039b8e087ce38f2500927b9e4ed003a48bbc3e8cc5ebb860395cad65af4f36d8cb19032a4e3f0647d11de; JSESSIONID=BAF34A7C54E2C18DEB074BB2F5786601.MG1; NEW_VISITOR=; RETURNING_VISITOR=; csrf=H6nlEklHgMh2A_62wxv3HK7w_pTYDBk-9GC2C4mZLHQ:AAABi1Sl1kM:JrxaN6TSmeb6pCGVOxE-oA; TS019866be=016eb44b02f5e6e619bffcab75be9f21720362880359ef45a3cbdda6ef39b2e82508f83e4302639e5cef6953844be00e94cb96566e4a5d901b226b6d59f215a1c9e475fe4564b172adaf6ad4adfbd0e1348bd338720de144079699ef6aad63eda8d645e492c4bf08cb5c8ca935d2593a9ce07b2d2f479f3c65f68010cae2a80d2383f7cfc61a214efef9dacff347452c1305302620f3964cad6705bfbd787ab701bab58654; TSaa745ca8027=083e718dc9ab200093d1de1820bbae90bc46172682ce295b9e84cd15429bbd9289d010a2c246f7560836132fcc11300098a4a2384818b66e27a26ea7f81769355be4ef8ad6d27f547b21a06ee2ecfa30024af1c5a87fdd45f7a6c236f914e888",
        "Host": "www.iberinform.es",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"
    }
    #res = requests.get(url = (BASE_URL + url), headers= REQUEST_HEADER, cookies=cookies)
    res = requests.get(url = test_url, headers=REQUEST_HEADER)
    html = res.text
    soup = bs(html, 'lxml')
    data_container = soup.find('div', attrs={'xpath' : '/html/body/div/main/section[3]/div/div[2]'})
    print(data_container)
    pass
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    #ARREGLAR


if __name__ == "__main__":
    #soup = open_browser()
    #result_extract_data = extract_data(soup)
    #data_all_companies, company_url = result_extract_data[0], result_extract_data[1]

    test_url = 'https://www.iberinform.es/empresa/778752/viveros-gimeno-valladolid'
    extract_data_by_company(test_url)
    
    