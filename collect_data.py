import time
import requests
import csv
from datetime import datetime
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from db_operations import write_in_db
import pandas as pd


def collect_data():
    partners_start = []
    with open('test_data_file.txt', 'r') as file:
        partners_start = file.read()

    partners = list(partners_start.split(sep=','))

    ua = UserAgent()
    url = 'https://zachestnyibiznes.ru/search'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "User-agent": ua.random
    }

    #Запись заголовков в файл
    with open('data_base_file.csv', 'w', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(
            (
                'Наименование организации',
                'Ссылка в реестре',
                'Должность руководителя',
                'ФИО руководителя',
                'Телефоны',
                'Emails',
                'Адрес',
                'Сайты',
                'Дата основания',
                'Об организации',
                'Дата обновления информации'
            )
        )

    #Selenium part
    chrome_options = Options()
    service = Service("D:/proectus/Praktika/chromedriver.exe")
    browser = webdriver.Chrome(options=chrome_options)


    try:
        browser.get(url=url)
        time.sleep(1.5)

        for partner in partners:
            input_tab = browser.find_element('xpath', '//*[@id="autocomplete-0-input"]')
            input_tab.send_keys(partner)
            input_tab.send_keys(Keys.ENTER)

            time.sleep(1.5)

            browser.find_element('xpath', '//*[@id="serach-filters-block"]/div[3]/p').click()
            browser.find_element('xpath', '//*[@id="status-filter-serach"]/div/label[1]').click()
            time.sleep(1.4)

            # Soup part
            soup = BeautifulSoup(browser.page_source, 'lxml')
            organisations = soup.find_all('div', class_="background-grey-blue-light p-15 b-radius-5 m-b-20")

            i = 1
            if organisations:
                for org in organisations:
                    link = 'https://zachestnyibiznes.ru' + org.find('p', class_="no-indent m-b-5 f-s-16 c-black").find('a', class_="no-underline-full").get('href')
                    name = org.find('p', class_="no-indent m-b-5 f-s-16 c-black").text

                    browser.get(url=link)
                    time.sleep(1)
                    try:
                        browser.find_element('xpath', '//*[@id="contacts_main_total"]/div[1]/div[1]/p[2]/a[1]/span').click()
                    except:
                        pass
                    time.sleep(1)

                    # ФИО руководителя
                    directors_name = soup.find_all('p', class_="no-indent m-b-5 c-black")[i]
                    i += 4

                    inner_res = requests.get(url=link, headers=headers)
                    inner_soup = BeautifulSoup(inner_res.text, 'lxml')

                    # Должность руководителя
                    try:
                        directors_spec = browser.find_element('xpath', '//*[@id="main-total-card"]/div/div[7]/div[1]/div[4]/p[2]/small').text
                    except:
                        directors_spec = 'Не указана должность руководителя'
                    # Телефоны
                    try:
                        phones = browser.find_element('xpath', '//*[@id="contacts_main_total"]/div[1]/div[1]/p[2]').text
                    except:
                        phones = 'Не указан телефон'
                    # Email
                    try:
                        emails = browser.find_element('xpath', '//*[@id="contacts_main_total"]/div[1]/div[2]/p[2]').text
                    except:
                        emails = 'Не указан Email'
                    # Адрес
                    try:
                        address = inner_soup.find('span', itemprop="address").text
                    except:
                        address = 'Не указан Адрес'
                    # Сайт
                    try:
                        sites = browser.find_element('xpath', '//*[@id="contacts_main_total"]/div[1]/div[3]/p[2]').text
                    except:
                        sites = 'Не указан Сайт'
                    # Дата основания
                    try:
                        birth_date = browser.find_element('xpath', '//*[@id="main-total-card"]/div/div[7]/div[1]/p[2]').text
                    except:
                        birth_date = 'Не указана дата основания'
                    # Об организации
                    try:
                        about = inner_soup.find('div', id="contacts_main_total").find('div', class_="col-md-12").text
                    except:
                        about = 'Нет информации об оршанизации'

                    with open('data_base_file.csv', 'a', encoding='utf-8') as file:
                        writer = csv.writer(file)
                        writer.writerow(
                            (
                                name.replace('\n', ''),
                                link,
                                directors_spec,
                                directors_name.text.replace('\n', ''),
                                phones.replace('\n', ''),
                                emails.replace('\n', ''),
                                address.replace('\n', ''),
                                sites.replace('\n', ''),
                                birth_date,
                                about.replace('\n', ''),
                                datetime.now().date()
                            )
                        )

                    update_date = str(datetime.now().date())
                    write_in_db(
                                "'"+name.replace('\n', '').replace('"', '')+"'",
                                "'"+link.replace('\n', '')+"'",
                                "'"+directors_spec.replace('\n', '')+"'",
                                "'"+directors_name.text.replace('\n', '')+"'",
                                "'"+phones.replace('\n', '').replace(' ', '-')+"'",
                                "'"+emails.replace('\n', '')+"'",
                                "'"+address.replace('\n', '')+"'",
                                "'"+sites.replace('\n', '')+"'",
                                "'"+birth_date.replace('.', '-')+"'",
                                "'"+about.replace('\n', '')+"'",

                    )
                    browser.execute_script("window.history.go(-1)")

                    time.sleep(2)
            else:
                pass

            time.sleep(1.5)
            browser.find_element('xpath', '//*[@id="autocomplete-top"]/div/form/div[3]/button').click()
            time.sleep(3)

    except Exception as ex:
        print(ex)
    finally:
        browser.close()
        browser.quit()

