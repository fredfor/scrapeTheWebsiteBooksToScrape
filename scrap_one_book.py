### phase 1 Exigences du système de surveillance des prix  http://course.oc-static.com/projects/Python+FR/P2+-+Utilisez+les+bases+de+Python+pour+l'analyse+de+march%C3%A9/Python_P2_FR_Requirements.pdf

import requests #import du paquet requests pour faire des requêtes HTTP
from bs4 import BeautifulSoup  # BeautifulSoup, composant de BS4, est une bibliothèque qui facilite la récupération d'informations à partir de pages Web
import re #utilisation des regex dans ce fichier
import csv #utilisation de la création des csv dans ce fichier
from pathlib import Path # permet de manipuler les chemins des systèmes de fichiers
import os # pour interagir (création de fichiers) avec le système d'exploitation 
from termcolor import colored #pour formater les résultats dans le terminal
from termcolor import cprint #pour formater les résultats dans le terminal

STAR_MAPPING = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5} # création d'un dictionnaire permettant d'interpréter les class du nombre d'étoiles (les dictionnnaires se mettent au début d'un fichier)

### STEP 1 : demander à l'utilisateur du programme quelle est l'URL de la page du livre à scraper
while True :

    print("Renseignez l'URL de la page du livre que vous souhaitez scraper puis appuyez sur Entrée (ex : http://books.toscrape.com/catalogue/worlds-elsewhere-journeys-around-shakespeares-globe_972/index.html)")
    url = input()


    ### STEP 2 : Le programme lance une requête get sur l’url et met la réponse dans un objet (ici :  « response ») s'il n'y a pas d'erreur de saisie
    try: # si pas de message d'erreur
        response = requests.get(url)
        response.encoding="utf-8" # car pas UTF-8 dans le header de la réponse http

        ### STEP 3 : recherche des éléments à collecter si réponse = 200
        if response.ok:
            soup = BeautifulSoup(response.text, 'lxml')# réponse parsée par BeautifulSoup à l'aide du parseur lxml
            # upc = soup.find('table', {'class': 'table-striped'}).findAll('th')[0].text # recherche d'une table avec sa class en 2ème argument (cet argument est un dicionnaire) + recherche à l'intérieur du premier td
            upc_value = soup.find('table', {'class': 'table-striped'}).findAll('td')[0].text # recherche d'une table avec sa class en 2ème argument (cet argument est un dicionnaire) + recherche à l'intérieur du premier td
            title = soup.find('h1').text
            # price_including_tax = soup.find('table', {'class': 'table-striped'}).findAll('th')[2].text
            price_including_tax_value = soup.find('table', {'class': 'table-striped'}).findAll('td')[2].text
            # price_excluding_tax = soup.find('table', {'class': 'table-striped'}).findAll('th')[3].text
            price_excluding_tax_value = soup.find('table', {'class': 'table-striped'}).findAll('td')[3].text
            number_available = soup.find('table', {'class': 'table-striped'}).findAll('td')[5].text
            number_available_value =  re.findall(r'\d+', number_available)[0] # \d+ selectionne tous les chiffres séquentiels
            # product_description = soup.find('h2').text
            product_description_value = soup.find('div', {'id': 'product_description'}).find_next_sibling('p').text  # Quelle galère pour cibler celui-là !!!
            category = soup.find('ul', {'class': 'breadcrumb'}).findAll('a')[2].text
            review_rating = soup.select_one('.star-rating').attrs['class'][1]# retourne {'class': ['star-rating', 'Three']} => grosse galère dans le print car pas possible d'avoir un dictionnaire dans la liste => str + obtenir seulement le dernier mot de la liste des classes !
            review_rating_value = str(STAR_MAPPING[review_rating])
            image_url = soup.find('div', {'id': 'product_gallery'}).find('img')['src'][5:]
            image_url_value = 'http://books.toscrape.com' + image_url 

            ### STEP 4 : conception d'un dictionnaire qui permettra d'éviter les erreurs de champs dans le fichier CSV produit (les descriptions des produits sont truffées de pièges ;-)
            en_tete = ['product_page_url', 'universal_ product_code', 'title', 'price_including_tax', 'price_excluding_tax', 'number_available', 'product_description', 'category', 'review_rating', 'image_url']
            datas = [url, upc_value, title, price_including_tax_value[1:], price_excluding_tax_value[1:], number_available_value, product_description_value, category, review_rating_value, image_url_value]
            dict_from_list = dict(zip(en_tete, datas))# passer par un dictionnaire pour mieux traiter la production du csv
            # print(dict_from_list)

            ### STEP 5 : impression des datas dans un dossier ad-hoc (et création de celui-ci s'il n'existe pas déjà)
            current_directory = os.getcwd()
            new_directory= Path(current_directory + "/Datas(CSV_Books_one_by_one)").mkdir(exist_ok=True)
            new_directory_path = Path("./Datas(CSV_Books_one_by_one)")
            with open(os.path.join(new_directory_path, title +'_infos.csv'), 'w', newline='', encoding='utf-8') as outfile: #utf_8_sig : https://stackoverflow.com/questions/46551955/python-3-csv-utf-8-encoding
                fieldnames = en_tete
                writer = csv.DictWriter(outfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerow(dict_from_list)

                ### STEP : informations un peu mises en forme lisibles directement dans le terminal
                print('\nVoici les données recueillies pour le livre "' + title + '" : \n')
                # print(dict_from_list)
                [print(colored(key.capitalize(), 'yellow'),':',value,"\n") for key, value in dict_from_list.items()]
                cprint('NB :', 'white', 'on_magenta', attrs=["blink", "underline"], end = ' ') 
                cprint(' Un fichier CSV contenant les datas du livre "' + title + '" a également été créé dans le dossier "Datas(CSV_Books_one_by_one)"', 'white', 'on_magenta')
                print("\nFaites CTRL + C pour terminer le programme ou lancez une nouvelle requête.")

    ### STEP 2 (bis) : Le programme renvoie un message d'erreur s'il y a une erreur de saisie
    except Exception:
        print("Merci de renseigner une URL valide")
