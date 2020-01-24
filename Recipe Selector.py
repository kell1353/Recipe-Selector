import os
import requests
from bs4 import BeautifulSoup

def createDict(url):
    global recipe
    urlEnd = url.split('/')[-2]
    recipe = ''
    for i in urlEnd.split('-'):
        cap = i.capitalize()
        recipe += str(cap)

        

url = 'https://www.budgetbytes.com/'
url2 = 'https://www.budgetbytes.com/monterey-chicken-skillet/'
url3 = 'https://www.budgetbytes.com/easy-cilantro-lime-chicken/'

urls= [url2, url3]

dicts = []
for url in urls:
    createDict(url)
    dicts.append(recipe)
recipes = dict.fromkeys(dicts, {})


for i in range(0,2):
    createDict(urls[i])
    site = requests.get(urls[i])
    text = site.content
    soup = BeautifulSoup(text, 'html.parser')

    titles = []
    for h2 in soup.findAll('h2'):
        titles.append(h2.text.strip())
    recipes[recipe]['Title'] = titles[0]

    for div in soup.findAll('div', {'class' : "wprm-recipe-summary wprm-block-text-normal"}):
        summary = div.text.strip()
        recipes[recipe]['Summary'] = summary

    for rating in soup.findAll('div', {'class' : "wprm-recipe-rating-details wprm-block-text-normal"}):
        rating = rating.text.strip()
        recipes[recipe]['Rating'] = rating


    for span in soup.findAll('span', {'class' : "wprm-recipe-recipe_cost wprm-block-text-normal"}):
        cost = span.text.strip()
        recipes[recipe]['Cost'] = cost
    for time in soup.findAll('span', {'class' : "wprm-recipe-time wprm-block-text-normal"}):
        time = time.text.strip()
        recipes[recipe]['Cook Time'] = time
    for servings in soup.findAll('div', {'class' : "wprm-recipe-servings-container wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-normal"}):
        servings = servings.text.strip()
        recipes[recipe]['Servings'] = servings


    ingredients = []
    for span in soup.findAll('li', {'class' : "wprm-recipe-ingredient"}):
        ingredients.append(span.text.strip())
        recipes[recipe]['Ingredients'] = ingredients

    instructions = []
    for ul in soup.findAll('ul', {'class' : "wprm-recipe-instructions"}):
        lis = ul.findAll('li')
    i = 1
    for li in lis:
        instructions.append(str(i) + '.) ' + str(li.text.strip()))
        recipes[recipe]['Instructions'] = instructions
        i += 1

    #print(recipes[recipe])
print(recipes)

soup2 = site.headers
print(soup2['Last-Modified'])    #Thu, 23 Jan 2020 06:09:25 GMT


txt = soup.findAll(text=True)
output = ''
blacklist = [
	'[document]',
	'noscript',
	'header',
	'html',
	'meta',
	'head', 
	'input',
	'script']
##for t in txt:
##    if t.parent.name not in blacklist:
##        output += '{} '.format(t)
##print(output)

