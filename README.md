# Scrape the website [BooksToScrape](http://books.toscrape.com/)
This project is the result of an exercise as part of a Python training course delivered by [OpenClassrooms](https://openclassrooms.com/fr/paths/585-developpement-d-une-application-avec-python)(PROJET 2). It contains 4 scripts to extract :
* the data of a single book on the site by entering its URL ([Script n°1](/scrap_one_book.py)),
* the data of all the books of a category by entering its URL ([Script n°2](/scrap_one_category.py)),
* the data of all the books of the site, classified by category ([Script n°3](/scrap_all_categories.py)),
* the data of all the books of the site with their images, classified by category ([Script n°4](/scrap_all_categories_with_img.py)).
Each script produces one or more CSV files.
## Technologies
This project uses [Python 3.8.10](https://www.python.org/downloads/) and some dependencies whose installation will be facilitated with the [requirements.txt](/requirements.txt) file.
## Installation
Clone this repository...
```
$ git clone https://github.com/fredfor/scrapeTheWebsiteBooksToScrape.git
```
...or dowload and extract the [ZIP file](https://github.com/fredfor/scrapeTheWebsiteBooksToScrape/archive/refs/heads/main.zip) of the projet.

In your folder, create a virtual environment that you can call "env" :
```
$ python3 -m venv env
```
Activite it :
```
$ source env/bin/activate
```
Install the dependencies:
```
$ pip install -r requirements.txt
```
## Use the scripts
To extract the **data of a single book**, run the [Script n°1](/scrap_one_book.py) and follow the instructions (you'll need the url of the book of your choice, ex: http://books.toscrape.com/catalogue/worlds-elsewhere-journeys-around-shakespeares-globe_972/index.html). You will be able to see the data directly on your console and a folder named "Datas(CSV_Books_one_by_one)" will be created. It will contain one CSV file per scraped book.
```
$ python3 scrap_one_book.py
```
To extract the **data of all the books of a category**, run the [Script n°2](/scrap_one_category.py) and follow the instructions (you'll need the url of the category of your choice, ex: http://books.toscrape.com/catalogue/category/books/nonfiction_13/index.html). A folder named "Datas(CSV_Categories_one_by_one)" will be created. It will contain one CSV file per scraped category
```
$ python3 scrap_one_category.py
```
To extract the **data of all the books of the website**, run the [Script n°3](/scrap_all_categories.py). A folder named "Datas(CSV_AllCategories)" will be created. It will contain one CSV file for each category
```
$ python3 scrap_all_categories.py
```
To extract the **data of all the books of the website with their image**, run the [Script n°4](/scrap_all_categories_with_img.py). A folder named "Datas(CSV_AllCategories)" will be created. It will contain one sub-folder with a CSV file and all the images of the books for each category 
```
$ python3 scrap_all_categories_with_img.py
```