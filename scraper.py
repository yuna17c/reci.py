# SCRAPER PRACTICE THIGNS ARE HERE

from bs4 import BeautifulSoup
import requests
# with open(r"C:\Users\Yuna\OneDrive\Documents\yuna17c.github.io\portfolio\index.html") as html_file:
#     soup1 = BeautifulSoup(html_file, 'lxml')
source = requests.get('https://www.allrecipes.com/recipe/277143/jalapeno-bacon-stuffing/').text
soup = BeautifulSoup(source, 'lxml')

# print(soup.prettify())
for div in soup.find_all('div'):
    title = div.get_text()
    if "ingredients" in title.lower() or "ingredient" in title.lower():
        print("ingredients header:", div)
# title = soup.find_all('div')
# print(title)

# match = soup.title 
# print(match)

# first_div = soup.div
# print(first_div)

# prj_list = soup.find('div', class_='contact-head')
# print(prj_list)

# headline = prj_list.h1.text
# detail = prj_list.h2.text
# print(headline, detail)

# for project in soup.find_all('div',class_='prj' ):
#     prj_name = project.find('div', class_='top').h1.text 
#     print(prj_name)