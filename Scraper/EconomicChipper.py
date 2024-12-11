from selenium import webdriver
from bs4 import BeautifulSoup
import time

#no more need for get_page and start() because biutifulsoup on top this works

def get_url(): #honestly idk if I should search by categ or by name
    url_arr = []
    #TO DO
    return  url_arr

def scrape_data(url):
    driver = webdriver.Chrome()
    driver.get(url)

    #scroll and sleeping 3 sec in case of lag
    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    #trying really hard to scroll
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')
    table = soup.find('table', class_='table table-bordered table-striped table-white table-bilant')

    #data is an array of the table contents but all even positions are indicators
    #for processing we will only use the odd positions
    data = []
    for row in table.find_all('tr')[1:]:
        cols = row.find_all('td')
        if len(cols) == 8:
            year = cols[0].text.strip()
            cifra_afaceri = cols[1].text.strip().replace('\xa0', '')
            profit_net = cols[2].text.strip().replace('\xa0', '')
            datorii = cols[3].text.strip().replace('\xa0', '')
            active_imobilizate = cols[4].text.strip().replace('\xa0', '')
            active_circulante = cols[5].text.strip().replace('\xa0', '')
            capitaluri_proprii = cols[6].text.strip().replace('\xa0', '')
            angajati = cols[7].text.strip().replace('\xa0', '')
            data.append({
                'Year': year,
                'Cifra Afaceri': cifra_afaceri,
                'Profit Net': profit_net,
                'Datorii': datorii,
                'Active Imobilizate': active_imobilizate,
                'Active Circulante': active_circulante,
                'Capitaluri Proprii': capitaluri_proprii,
                'Angajati': angajati
            })

    driver.quit()
    return data
