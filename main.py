import requests
from bs4 import BeautifulSoup
import csv 
import os
import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
}

def get_html(url):
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        all_cards = soup.find_all('div', class_='card')

        data = []
        
        for card in all_cards:
            try:
                title_element = card.find('h2', class_='card-title')
                title = title_element.text.strip() if title_element else 'N/A'
            except:
                title = None

            try:
                card_img = card.find('img').get('src')
            except:
                card_img = None
            
            try:
                price_element = card.find('li')
                price = price_element.find('b').text.strip() if price_element else 'N/A'              
            except:
                price = None

            try:
                categories_element = card.find_all('li')[1].find_all('span')[1]
                # print(categories_element.text)
                categories = categories_element.text if categories_element else 'N/A'
            except:
                categories = None

            try:
                age_element = card.find_all('li')[2].find_all('span')[1]
                # print(age_element)
                age = age_element.text.strip() if age_element else 'N/A'
            except:
                age = None
            
            
            try:
                company_link = card.find_all('li')[3].find('a').get('href')
                
            except:
                company_link = None
            
            try:
                company_element = card.find_all('li')[3].find('a')
                company = company_element.text if company_element else 'N/A'
            except:
                company = None
            
            try:
                address_element = card.find_all('li')[4].find_all('span')[1]
                address = address_element.text if address_element else 'N/A'
            except:
                address = None

            card_data = {
                'title': title,
                'card_img': card_img,
                'price': price,
                'categories': categories,
                'age': age,
                'company': company,
                'company_link': company_link,
                'address': address
            }
            
            data.append(card_data) 
            print('Success:', card_data['title'])
        
        return data

    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")




def write_to_csv(data):
    fieldnames = ['title', 'card_img', 'price', 'categories', 'age', 'company', 'company_link', 'address']
    with open('result.csv', 'a', encoding='utf-8', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        for item in data:
            writer.writerow(item)  

def get_last_page_number(url):
    try:
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'lxml')
        pagination = soup.find('ul', class_='pagination')
        last_page_link = pagination.find_all('a')[-2]  
        last_page_number = int(last_page_link.text)
        return last_page_number
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")
        return None

def main():
    base_url = 'https://www.education.ua/courses/?search=&city=0&kind=0'
    last_page_number = get_last_page_number(base_url)
    if last_page_number is None:
        return
    
    if not os.path.isfile('result.csv'):
        fieldnames = ['title', 'card_img', 'price', 'categories', 'age', 'company', 'company_link', 'address']
        with open('result.csv', 'w', encoding='utf-8', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()

    for page in range(1, last_page_number + 1):
        url = f'{base_url}&page={page}'
        data = get_html(url)
        write_to_csv(data)
        time.sleep(2)

if __name__ == '__main__':
    main()