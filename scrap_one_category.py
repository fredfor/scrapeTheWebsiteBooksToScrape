### phase 2 Exigences du système de surveillance des prix  http://course.oc-static.com/projects/Python+FR/P2+-+Utilisez+les+bases+de+Python+pour+l'analyse+de+march%C3%A9/Python_P2_FR_Requirements.pdf
import requests 
from bs4 import BeautifulSoup  
import re 
import csv 
from pathlib import Path
import os
from termcolor import cprint

STAR_MAPPING = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}


### STEP 1 : demander à l'utilisateur du programme quelle est l'URL de la catégorie à scraper
while True :

    print("Renseignez l'URL de la catégorie que vous souhaitez scraper puis appuyez sur Entrée (ex : http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html)")
    url = input()
    url = url[:-10]# supprime "index.html" de l'url de la catégorie
    category_name = url[51:-1]#pour avoir le nom de la catégorie, utile pour construire le nom du fichier CSV pour chaque catégorie
    # print(url)
    # print(category_name)
    
    try: # si pas de message d'erreur
        ### STEP 2 une boucle while pour aller chercher toutes les urls des pages d'une catégorie (traitement des next_links) et les mettre dans une liste
        all_urls_pages=[]
        response = requests.get(url)
        if response.ok:
            all_urls_pages.append(url)
            soup = BeautifulSoup(response.text, 'lxml')
            if soup.find('li', {'class': 'next'}) :
                while True :
                    next_link = str(soup.find('li', {'class': 'next'}).findAll('a')[0])[9:][:-10] # supprime les 9 premiers caractères de la chaine et les 10 derniers
                    new_url = url + next_link
                    new_response = requests.get(new_url)
                    all_urls_pages.append(new_url)
                    soup = BeautifulSoup(new_response.text, 'lxml')
                    if soup.find('li', {'class': 'next'}) :
                        next_link = str(soup.find('li', {'class': 'next'}).findAll('a')[0])[9:][:-10] 
                    else :
                        break
            # if not soup.find('li', {'class': 'next'}) :
            #     print('no next-link in this page')
        # print(all_urls_pages)

        ### STEP 3 : une boucle pour avoir toutes les urls de tous les livres de toutes les pages d'une catégorie et les mettre dans une liste
        products_pages_urls = [] 
        for url_page in all_urls_pages :
            response = requests.get(url_page)
            #print(response) 
            soup = BeautifulSoup(response.text,'lxml') 
            articles = soup.findAll('article') # recherche de toutes les balises <article> de la page
            
            ### STEP 4 : boucle pour trouver les balises <a> de chaque article :
                #+ selectionner l'attribut href de chaque lien
                #+ ajouter l'attribut href à la liste avec la fonction append
                #+ concaténation avec l'url de base du site + les urls
        
            for article in articles:
                a = article.find('a')
                product_page_url = a['href'][8:]# supprime les huit premiers caractères de la chaine, les "../../.." qui se trouvent devant toutes les urls => peut se faire avec replace (= methode le clase str)
                products_pages_urls.append('http://books.toscrape.com/catalogue' + product_page_url)




        ### STEP 5 : impression des datas dans un dossier ad-hoc (et création de celui-ci s'il n'existe pas déjà)
        current_directory = os.getcwd()
        new_directory= Path(current_directory + "/Datas(CSV_Categories_one_by_one)").mkdir(exist_ok=True)
        new_directory_path = Path("./Datas(CSV_Categories_one_by_one)")
        en_tete = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
        with open(os.path.join(new_directory_path, category_name +'_AllBooksInfos.csv'), 'w', newline='', encoding='utf_8_sig') as outfile: #utf_8_sig : https://stackoverflow.com/questions/46551955/python-3-csv-utf-8-encoding
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
            cprint('Un fichier CSV contenant les datas de la catégorie "' + category_name + '" a été créé dans le dossier "Datas(CSV_Categories_one_by_one)"', 'white', 'on_magenta')
            print("\nFaites CTRL + C pour terminer le programme ou lancez une nouvelle requête.")

    except Exception: # si message d'erreur après saisie par l'utilisateur
        print("Merci de renseigner une URL valide")





