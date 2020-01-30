import os
import pandas as pd
import openpyxl
import ast
import requests
import webbrowser
from bs4 import BeautifulSoup

'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'

def createRecipe(url):
    global recipe
    urlEnd = url.split('/')[-2]
    recipe = ''
    for i in urlEnd.split('-'):
        cap = i.capitalize()
        recipe += str(cap)

        
def createDict():
    'Create url dataframe from the corresponding excel file and add them to a list to be evaluated'
    path = 'C:/Users/Austin Keller/Desktop/Coding Files/Recipe Parser'
    os.chdir(path)

    urls = []
    df = pd.read_excel('RecipeList.xlsx', sheet_name = 'Recipe List')
    for index, row in df.iterrows():
        #print (row["Recipes"])
        urls.append(row["Recipes"])

    ##########################################################################################

    'Create the dictionaries for each recipe in the dataframe'
    recipes = {}
    for i in range(0,len(urls)):
        createRecipe(urls[i])
        site = requests.get(urls[i])
        text = site.content
        soup = BeautifulSoup(text, 'html.parser')

        # Grab the name of the dish
        titles = []
        for h2 in soup.findAll('h2'):
            titles.append(h2.text.strip())
        recipes[recipe] = {'Title': titles[0]}
        # Grab a photo of the dish
        image = soup.findAll('img')[4]['data-lazy-src']
        recipes[recipe]['Image'] = image
        # Grab the summary of the dish
        for div in soup.findAll('div', {'class' : "wprm-recipe-summary wprm-block-text-normal"}):
            summary = div.text.strip()
            recipes[recipe]['Summary'] = summary
        # Grab the consumer rating of the dish
        for rating in soup.findAll('div', {'class' : "wprm-recipe-rating-details wprm-block-text-normal"}):
            rating = rating.text.strip()
            recipes[recipe]['Rating'] = rating

        # Grab the estimated cost of the dish
        for span in soup.findAll('span', {'class' : "wprm-recipe-recipe_cost wprm-block-text-normal"}):
            cost = span.text.strip()
            recipes[recipe]['Cost'] = cost
        # Grab the estimated cook time of the dish
        for time in soup.findAll('span', {'class' : "wprm-recipe-time wprm-block-text-normal"}):
            time = time.text.strip()
            recipes[recipe]['Cook Time'] = time
        # Grab the default number of servings the dish provides
        for servings in soup.findAll('div', {'class' : "wprm-recipe-servings-container wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-normal"}):
            servings = servings.text.strip()
            recipes[recipe]['Servings'] = servings

        # Grab the list of ingredients required to make the dish
        ingredients = []
        for span in soup.findAll('li', {'class' : "wprm-recipe-ingredient"}):
            ingredients.append(span.text.strip())
            recipes[recipe]['Ingredients'] = ingredients

        # Grab the list of instructions required to make the dish
        instructions = []
        for ul in soup.findAll('ul', {'class' : "wprm-recipe-instructions"}):
            lis = ul.findAll('li')
        i = 1
        for li in lis:
            instructions.append(str(i) + '.) ' + str(li.text.strip()))
            recipes[recipe]['Instructions'] = instructions
            i += 1

        print(recipes[recipe]['Summary'])

##########################################################################################
    'Retrieve the workbook and worksheet objects.'
    workbook  = openpyxl.load_workbook('RecipeList.xlsx')
    worksheet = workbook['Full Dictionary']

    'Save full recipes dictionary to cell A1 in the Full Dictionary sheet. (In case the site changes)' 
    worksheet['A1'] = str(recipes)
    workbook.save('RecipeList.xlsx')
    workbook.close()

############################################################################################

def generateHTML(recipe):
    'Retrieve the workbook and worksheet for the dictionary objects.'
    workbook  = openpyxl.load_workbook('RecipeList.xlsx')
    worksheet = workbook['Full Dictionary']
    recipes = ast.literal_eval(worksheet['A1'].value)

    'Split the lists of ingredients and instructions into single lines'
    ingredientsList = ''
    for i in recipes[recipe]['Ingredients']:
        ingredientsList += "<p>" + str(i) + "</p>"
    instructionsList = ''
    for i in recipes[recipe]['Instructions']:
        instructionsList += "<p>" + str(i) + "</p>"

    htmlFile = open('Generated Recipes.html','w')

    html = """
    <html>
            <head>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                            * {box-sizing: border-box;}

                            /* Create two columns that float next to each other */
                            .column1 {float: left; width: 65%; padding: 10px; height: 300px;}
                            .column2 {float: left; width: 35%; padding: 10px; height: 100%;}

                            .header {padding: 10px;}

                            /* Clear floats after the columns */
                            .row:after {content: ""; display: table; clear: both;}
                    </style>
            </head>
            
            <body>
            <div class="header">
                    <h1 padding: 100px>Recipes</h1>
            </div>

            <div class="row">
                    <div class="column1">
                            <h2>""" + recipes[recipe]['Title'] + """</h2>
                            <img src =""" + recipes[recipe]['Image'] + """>
                            <h3>Summary</h3>
                            <p>""" + recipes[recipe]['Summary'] + """</p>
                            <h3>Rating: """ + recipes[recipe]['Rating'] + """</h3>
                            <h3>Cost: """ + recipes[recipe]['Cost'] + """</h3>
                            <h3>Cook Time: """ + recipes[recipe]['Cook Time'] + """</h3>
                            <h3>""" + recipes[recipe]['Servings'] + """</h3>
                            <h3>Instructions</h3>
                            <p>""" + instructionsList + """</p>
                    </div>
                    <div class="column2" style="background-color:#bbb;">
                            <h2>Ingredients</h2>
                            <p>""" + ingredientsList + """</p>
                    </div>
            </div>
            </body>
    </html>"""

    htmlFile.write(html)
    htmlFile.close()
    webbrowser.open_new_tab('Generated Recipes.html')
generateHTML('MontereyChickenSkillet')
