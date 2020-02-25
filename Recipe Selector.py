import os
import pandas as pd
import openpyxl
import ast
import requests
import webbrowser
from bs4 import BeautifulSoup
import random

'https://www.crummy.com/software/BeautifulSoup/bs4/doc/'

path = 'C:/Users/Austin Keller/Desktop/Coding Files/Recipe Parser'
os.chdir(path)

def createRecipe(url):
    urlEnd = str(url).split('/')[-2]
    recipe = ''
    for i in urlEnd.split('-'):
        cap = i.capitalize()
        recipe += str(cap)
    return recipe


def getUrls(sheetName):
    'Create url dataframe from the corresponding excel file and add them to a list to be evaluated'
    urls = []
    df = pd.read_excel('RecipeList.xlsx', sheet_name = sheetName)
    for index, row in df.iterrows(): urls.append(row[sheetName])
    return urls


def getExcelDoc():
    global workbook; global worksheet
    'Retrieve the workbook and worksheet objects.'
    workbook  = openpyxl.load_workbook('RecipeList.xlsx')
    worksheet = workbook['Full Dictionary']

    
def createDict():
    'Retrive recipe url list from excel doc'
    types = ['Lunch_Dinner', 'Breakfast']

    'Create the dictionaries for each recipe in the dataframe'
    recipes = {'Lunch_Dinner': {}, 'Breakfast': {}}

    'Retrieve the workbook and worksheet for the dictionary objects.'
    getExcelDoc()

    ############### change start to last cell in dictionary | Also Delete lists in breakfast for new recipes ###############
    start = 2
    for t in types:
        urls = getUrls(t)
        for i in range(0, len(urls)):
            recipe = createRecipe(urls[i])
            site = requests.get(urls[i])
            text = site.content
            soup = BeautifulSoup(text, 'html.parser')

            worksheet['A'+str(start)+''] = str(recipe)
            worksheet['B'+str(start)+''] = str(urls[i])
            worksheet['C'+str(start)+''] = str(t)

            # Grab the name of the dish
            title = soup.find('h1').text.strip()
            recipes[t][recipe] = {'Title': title}
            worksheet['D'+str(start)+''] = str(title)
            # Grab a photo of the dish
            image = soup.findAll('img', {'class' : "attachment-200x200 size-200x200"})[0]['data-lazy-src']
            recipes[t][recipe]['Image'] = image
            worksheet['E'+str(start)+''] = str(image)
            # Grab the summary of the dish
            for div in soup.findAll('div', {'class' : "wprm-recipe-summary wprm-block-text-normal"}):
                summary = div.text.strip()
                recipes[t][recipe]['Summary'] = summary
                worksheet['F'+str(start)+''] = str(summary)
            # Grab the consumer rating of the dish
            for rating in soup.findAll('div', {'class' : "wprm-recipe-rating-details wprm-block-text-normal"}):
                rating = rating.text.strip()
                recipes[t][recipe]['Rating'] = rating
                worksheet['G'+str(start)+''] = str(rating)


            # Grab the estimated cost of the dish
            for span in soup.findAll('span', {'class' : "wprm-recipe-recipe_cost wprm-block-text-normal"}):
                cost = span.text.strip()
                recipes[t][recipe]['Cost'] = cost
                worksheet['H'+str(start)+''] = str(cost)
            # Grab the estimated cook time of the dish
            for time in soup.findAll('span', {'class' : "wprm-recipe-time wprm-block-text-normal"}):
                time = time.text.strip()
                recipes[t][recipe]['Cook Time'] = time
                worksheet['I'+str(start)+''] = str(time)
            # Grab the default number of servings the dish provides
            for servings in soup.findAll('div', {'class' : "wprm-recipe-servings-container wprm-recipe-block-container wprm-recipe-block-container-separate wprm-block-text-normal"}):
                servings = servings.text.strip()
                recipes[t][recipe]['Servings'] = servings
                worksheet['J'+str(start)+''] = str(servings)

            # Grab the list of ingredients required to make the dish
            ingredients = []
            for span in soup.findAll('li', {'class' : "wprm-recipe-ingredient"}):
                ingredients.append(span.text.strip())
                recipes[t][recipe]['Ingredients'] = ingredients
            worksheet['K'+str(start)+''] = str(ingredients)
            # Grab the list of instructions required to make the dish
            instructions = []
            for ul in soup.findAll('ul', {'class' : "wprm-recipe-instructions"}):
                lis = ul.findAll('li')
            j = 1
            for li in lis:
                instructions.append(str(j) + '.) ' + str(li.text.strip()))
                recipes[t][recipe]['Instructions'] = instructions
                j += 1
            worksheet['L'+str(start)+''] = str(instructions)

            start += 1
    'Retrieve the workbook and worksheet for the dictionary objects.'
    #getExcelDoc()

    'Save full recipes dictionary to cell A1 in the Full Dictionary sheet. (In case the site changes)' 
##    worksheet['A1'] = str(recipes)
    workbook.save('RecipeList.xlsx')
    workbook.close()
#createDict()



def generateHTML(Type, recipe):
    'Retrieve the workbook and worksheet for the dictionary objects.'
    getExcelDoc()
    #recipes = ast.literal_eval(worksheet['A1'].value)

    'Split the lists of ingredients and instructions into single lines'
    ingredientsList = ''
    for i in recipes[Type][recipe]['Ingredients']:
        ingredientsList += "<p>" + str(i) + "</p>"
    instructionsList = ''
    for i in recipes[Type][recipe]['Instructions']:
        instructionsList += "<p>" + str(i) + "</p>"

    htmlFile = open('Generated Recipes.html','w')
    #style = "font-family:georgia,garamond,serif;font-size:16px;font-style:italic;">
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
            
            <body style = "font-family: arial;">
            <div class="header">
                    <h1 padding: 100px>Recipes</h1>
            </div>

            <div class="row">
                    <div class="column1">
                            <h2>""" + recipes[Type][recipe]['Title'] + """</h2>
                            <img src =""" + recipes[Type][recipe]['Image'] + """>
                            <h3>Summary</h3>
                            <p>""" + recipes[Type][recipe]['Summary'] + """</p>
                            <h3>Cost: """ + recipes[Type][recipe]['Cost'] + """</h3>
                            <h3>Cook Time: """ + recipes[Type][recipe]['Cook Time'] + """</h3>
                            <h3>""" + recipes[Type][recipe]['Servings'] + """</h3>
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
#generateHTML('MontereyChickenSkillet')
#generateHTML('Lunch_Dinner', 'EasyCilantroLimeChicken')
#generateHTML('OnePotCreamyPestoChickenPasta')



def generateRandRecipes(Type, n):
    'Retrieve the workbook and worksheet for the dictionary objects.'
    getExcelDoc()
    #recipes = ast.literal_eval(worksheet['A1'].value)

    'Retrive recipe url list from excel doc'
    urls = getUrls(Type)

    randRec = random.sample(range(0, len(urls)), n)
    #randRec = random.sample(range(2, 5), n)
    columns, columnDiv, ingredientsList = '', '', ''
    for i in range(0, len(randRec)):
        recipe = createRecipe(urls[randRec[i]])

        ingredients = ast.literal_eval(worksheet["K"+ str(randRec[i])].value)
        for j in ingredients:
            ingredientsList += "<p>" + str(j) + "</p>"
        
        columns +=  """.column""" + str(i + 1) + """ {border-style: groove; float: left; width: """ + str(100/len(randRec)) + """%; padding: 10px; height: 60%;}"""
        #style ="position: absolute; top: 585px; width: 24%;"
        columnDiv += """<div class=""" + 'column' + str(i + 1) + """>
                                                   <h2>""" + worksheet['D'+ str(randRec[i])].value + """</h2>
                                                   <img src =""" + worksheet['E'+ str(randRec[i])].value + """ border = "2"; >
                                                   <h3> Summary </h3>
                                                   <p>""" + worksheet['F'+ str(randRec[i])].value + """</p>
                                           </div>"""

    htmlFile = open('Generated Recipes.html','w')
    #style = "font-family:georgia,garamond,serif;font-size:16px;font-style:italic;">
    html = """
    <html>
            <head>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                            * {box-sizing: border-box;}

                            /* Create two columns that float next to each other */
                            """ + columns + """

                            .header {padding: 10px;}

                            .img {position: absolute; left: 0px; top: 150px; z-index: -1;}
                            
                            /* Clear floats after the columns */
                            .row:after {content: ""; display: table; clear: both;}
                    </style>
            </head>
            
            <body style = "font-family: arial;">
                    <div class="header">
                            <h1 padding: 100px>Recipes</h1>
                    </div>

                    <div class="row">
                        """ + columnDiv + """
                    </div>
                    
                    <div class="row">
                        <h2> Necessary Ingredients </h2>
                        <p>""" + ingredientsList + """</p>
                    </div>         
            </body>
    </html>"""

    htmlFile.write(html)
    htmlFile.close()
    webbrowser.open_new_tab('Generated Recipes.html')
generateRandRecipes('Lunch_Dinner', 2)
 
