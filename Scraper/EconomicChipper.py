from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import pandas as pd
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

    username_input = driver.find_elements(By.XPATH, "//th[contains(text(), 'Domeniul de activitate preponderent (raportat în bilanț)')]//parent::tr//parent::tbody//tr//td")   
    print("test")
    #print(username_input)   
    #print(username_input[1].get_attribute('innerHTML'))
    
    category = username_input[1].get_attribute('innerHTML')[:2]
    
    driver.quit()
    return (data,category) #data is an array that acts like a map but use odd positions for row data vector

#sample data for ml testing
import csv


#print('----------------')
#urls=get_urls('01')
#print(urls)
#print('----------------')


def get_category_data():
    category_map=get_categories()
    print(category_map)

    scraped_categories = {'01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31','32','33', '34','35','36','37','38','39','40','41','42','43','44','45','46','47','48','49','50','51','52','53','54','55','56','57','58','59','60','61','62','63','64','65','66','67','68','69','70','71','72','73'}
    print(category_map.keys())
    for company_category in category_map.keys():
        if(company_category[0]=='a'): continue

        if(company_category in scraped_categories): continue
        #print(company_category)
        urls=get_urls(company_category)
        
        print("\n\n\n----------SCRAPING DATA FOR CATEGORY "+company_category+"----------\n\n\n")

        data_file = 'data_'+company_category+'.csv'
        print(data_file)
        for i in range(min(8, len(urls))):
            print("getting element #"+str(i)+" from list")
            data=scrape_data(urls[i])[0]
            print(data)
            # writing into a csv
            file=open(data_file,'a', newline='')
            writer = csv.writer(file)
            
            if i == 0:
                writer.writerow(data[0].keys())
            for row in data:
                writer.writerow(row.values())
            file.close()

    #am să fac mai întâi o probă cu 10 elemente din categoria 1

#print(scrape_data("https://www.listafirme.ro/frigoalex-service-srl-12527501/")[1])

def sanitise_input():
    categories = get_categories().keys()
    #andrei's code

def remove_zeros():
    categories = get_categories().keys() 

    for category_key in categories:
        if(category_key[0]=='a'): continue
        excluded_keys = {'33','73'}
        if(category_key in excluded_keys): continue

        data_file = 'data/data_'+category_key+'.csv'
        df = pd.read_csv(data_file)
        
        mask = df['Cifra Afaceri'] == 0
        df = df[~mask]
        df.to_csv(data_file, index=False)
        print(df)

sanitise_input()

def get_url_by_search(search_term):
    chrome_options = Options()
    chrome_options.add_argument("--headless")

    driver = webdriver.Chrome(options=chrome_options)
    url = 'https://www.listafirme.ro/'
    driver.get(url)


    search_box = driver.find_element(By.NAME, 'searchfor')
    search_box.send_keys(search_term)
    search_box.submit()

    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'clickable-row')))

    html_source = driver.page_source
    soup = BeautifulSoup(html_source, 'html.parser')

    base_url = 'https://www.listafirme.ro'
    first_row = soup.find('td', class_='clickable-row')
    first_url = None
    if first_row:
        data_href = first_row.get('data-href')
        if data_href:
            first_url = base_url + data_href

    driver.quit()
    return first_url

