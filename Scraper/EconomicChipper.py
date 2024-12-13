from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import time

# no more need for get_page and start() because biutifulsoup on top this works


def get_categories(): # get all categories in map output
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get('https://www.listafirme.ro/firme-domenii.asp?url=/21/d3.htm')

    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    data = {}
    tree_div = soup.find('div', id='treeDiv1')
    if tree_div:
        links = tree_div.find_all('a')
        for link in links:
            href = link.get('href')
            if href and href.startswith('/'):
                number = href.split('/')[1]
                text = link.text.strip()
                text = text.split(' ', 1)[1] if ' ' in text else text
                data[number] = text
                #literal python magic

    driver.quit()

    return data #data is a map of category number to category full name


def get_urls(categ_nr):  # search by category number
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    url = f'https://www.listafirme.ro/{categ_nr}/d1.htm'
    driver.get(url)

    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    url_arr = []
    base_url = 'https://www.listafirme.ro'
    rows = soup.find_all('td', class_='clickable-row')
    for row in rows:
        data_href = row.get('data-href')
        if data_href:
            full_url = base_url + data_href
            url_arr.append(full_url)

    driver.quit()
    return url_arr

def scrape_data(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)

    # scroll and sleeping 3 sec in case of lag
    SCROLL_PAUSE_TIME = 3
    last_height = driver.execute_script("return document.body.scrollHeight")

    # trying really hard to scroll
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

    # data is an array of the table contents but all even positions are indicators
    # for processing we will only use the odd positions
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
    return data #data is an array that acts like a map but use odd positions for row data vector

#sample data for ml testing
import csv

category_map=get_categories()
#print(category_map)
#print('----------------')
urls=get_urls('01')
#print(urls)
#print('----------------')
data=scrape_data(urls[0])
print(data)
# writing into a csv
file=open('data_sample.csv','w', newline='')
writer = csv.writer(file)
writer.writerow(data[0].keys())
for row in data:
    writer.writerow(row.values())
file.close()