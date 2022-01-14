from bs4 import BeautifulSoup
import requests
# with open(r"C:\Users\Yuna\OneDrive\Documents\yuna17c.github.io\portfolio\index.html") as html_file:
#     soup1 = BeautifulSoup(html_file, 'lxml')
source = requests.get('https://en.wikipedia.org/wiki/Roblox').text
soup = BeautifulSoup(source, 'lxml')
# print(soup.prettify())
title = soup.title 
print(title)
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