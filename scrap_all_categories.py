### phase 3 Exigences du système de surveillance des prix  http://course.oc-static.com/projects/Python+FR/P2+-+Utilisez+les+bases+de+Python+pour+l'analyse+de+march%C3%A9/Python_P2_FR_Requirements.pdf

import requests 
from bs4 import BeautifulSoup  
import re 
import csv 
from pathlib import Path
import os
from termcolor import cprint


STAR_MAPPING = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5} 

### STEP 1 : une boucle pour aller chercher toutes les urls des catégories
categories_urls=[]
# categories_names=[]
url = 'http://books.toscrape.com/' #url de la page à scraper
response = requests.get(url)
if response.ok:
    soup = BeautifulSoup(response.text, 'lxml')
    for (a) in soup.find('div', {'class': 'side_categories'}).findAll('a', href=True):
        categories_urls.append(url + a['href'][0:-10]) 
    categories_urls.pop(0) # le premier lien est "book" et ne mène à aucune catégorie => pop le fait sauter de la liste
    # categories_names.pop(0)
# print(categories_urls)
# print(categories_names)

### STEP 2 : une fonction pour obtenir toutes les données de tous les livres d'une catégorie dans une dictionnaire
def all_url_books_for_one_categorie(categorie_url):
    #toutes les urls des pages d'une catégorie + recherche d'un lien next
    all_urls_pages=[]
    url = categorie_url 
    response = requests.get(url)
    # print(url)
    category_name = url[51:-1]
    # print(category_name)
    if response.ok:
        all_urls_pages.append(url)
        soup = BeautifulSoup(response.text, 'lxml')
        if soup.find('li', {'class': 'next'}) :
            while True :
                next_link = str(soup.find('li', {'class': 'next'}).findAll('a')[0])[9:][:-10]
                #print(next_link) 
                new_url = categorie_url + next_link
                new_response = requests.get(new_url)
                all_urls_pages.append(new_url)
                soup = BeautifulSoup(new_response.text, 'lxml')
                if soup.find('li', {'class': 'next'}) :
                    next_link = str(soup.find('li', {'class': 'next'}).findAll('a')[0])[9:][:-10] 
                else :
                    break
   
        # toutes les urls des livres d'une catégorie
        products_pages_urls = []
        for url_page in all_urls_pages :
            response = requests.get(url_page)
            #print(response) 
            soup = BeautifulSoup(response.text,'lxml') 
            articles = soup.findAll('article') 
            for article in articles:
                a = article.find('a')
                product_page_url = a['href'][8:]
                products_pages_urls.append('http://books.toscrape.com/catalogue' + product_page_url)
        # print(products_pages_urls) 
        # toutes les données de chaque livre de la catégorie => un csv par catégorie

        current_directory = os.getcwd()
        new_directory= Path(current_directory + "/Datas(CSV_AllCategories)").mkdir(exist_ok=True)
        new_directory_path = Path("./Datas(CSV_AllCategories)")
        en_tete = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        with open(os.path.join(new_directory_path, 'all_books_infos_for_category_'+ category_name +'.csv'), 'w', newline='', encoding='utf-8') as outfile: 
            writer = csv.DictWriter(outfile, fieldnames = en_tete)
            writer.writeheader()
            for product_page_url in products_pages_urls:
                response_1 = requests.get(product_page_url)
                response_1.encoding="utf-8"
                soup = BeautifulSoup(response_1.text, 'lxml')
                upc_value = soup.find('table', {'class': 'table-striped'}).findAll('td')[0].text
                title = soup.find('h1').text
                price_including_tax_value = soup.find('table', {'class': 'table-striped'}).findAll('td')[2].text
                price_excluding_tax_value = soup.find('table', {'class': 'table-striped'}).findAll('td')[3].text
                number_available = soup.find('table', {'class': 'table-striped'}).findAll('td')[5].text
                number_available_value =  re.findall(r'\d+', number_available)[0]
                if soup.find('div', {'id': 'product_description'}):# le if car pas de description pour au moins un livre !
                    product_description_value = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text 
                category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text
                review_rating = soup.select_one('.star-rating').attrs['class'][1]
                review_rating_value = str(STAR_MAPPING[review_rating])
                image_url = soup.find('div', {'id': 'product_gallery'}).find('img')['src'][5:]
                image_url_value = 'http://books.toscrape.com' + image_url 
                data_values = [product_page_url, upc_value, title, price_including_tax_value[1:], price_excluding_tax_value[1:], number_available_value, product_description_value, category, review_rating_value, image_url_value]
                dict_from_list = dict(zip(en_tete, data_values))
                writer.writerow(dict_from_list)
            # print(dict_from_list)
    # print(all_urls_pages)
    # print(products_pages_urls)


### STEP 3 : appel de la fonction pour toutes les catégories
for categorie_url in categories_urls :  
    all_url_books_for_one_categorie(categorie_url)

cprint('Programme terminé. Un fichier CSV par catégorie a été créé dans le dossier "Datas(CSV_AllCategories)"', 'white', 'on_magenta')

