from bs4 import BeautifulSoup
import requests
import df_csv_writer as dcw

data_df = dcw.initialize_df()

def fetchDataFromRecipeWebsite(recipeLink):
        global data_df
        if recipeLink is not None and 'ultimatepaleoguide' in recipeLink:
            response = requests.get(recipeLink)
            if response.status_code == 200:
                recipeSiteHtml = response.text
            else:
                print("Failed to retrieve "+recipeLink+" webpage")
            siteSoup = BeautifulSoup(recipeSiteHtml,'lxml')
            
            title = siteSoup.find(class_='wprm-recipe-name').text if siteSoup.find(class_='wprm-recipe-name') is not None else ' '

            cooktime = siteSoup.find(class_='wprm-recipe-total_time').text \
                                            + ' ' + siteSoup.find(class_='wprm-recipe-prep_time-unit').text \
                                            if siteSoup.find(class_='wprm-recipe-total_time') is not None \
                                            and siteSoup.find(class_='wprm-recipe-prep_time-unit') is not None else ' '
            if cooktime.replace('minutes','').strip().isnumeric():
                cooktime = int(cooktime.replace('minutes','').strip())                
            else:
                cooktime = ''

            servings = siteSoup.find(class_='wprm-recipe-servings').text if siteSoup.find(class_='wprm-recipe-servings') is not None else ' '

            ingredient_items = siteSoup.find_all('li', class_='wprm-recipe-ingredient') 
            ingredients_list = []
            for ingredient_item in ingredient_items:
                            amount = ingredient_item.find(class_='wprm-recipe-ingredient-amount').text.strip() if ingredient_item.find(class_='wprm-recipe-ingredient-amount') else ' '
                            unit = ingredient_item.find(class_='wprm-recipe-ingredient-unit').text.strip() if ingredient_item.find(class_='wprm-recipe-ingredient-unit') else ' '
                            name = ingredient_item.find(class_='wprm-recipe-ingredient-name').text.strip() if ingredient_item.find(class_='wprm-recipe-ingredient-name') else ' '
                            full_ingredient = f"{amount} {unit} {name}"
                            ingredients_list.append(full_ingredient)
                            
            ingredients = '\n'.join(ingredients_list)

            mealtype = siteSoup.find(class_='wprm-recipe-course').text if siteSoup.find(class_='wprm-recipe-course') is not None else ' '

            instruction_elements = siteSoup.find_all('div', class_='wprm-recipe-instruction-text')
            instruction_list = [element.text.strip() for element in instruction_elements]
            instructions = '\n\n'.join(instruction_list)

            review = ''
            nutrient = ''
            
            row = [title,recipeLink,servings,cooktime,mealtype,review,\
                       ingredients[:-1],instructions[:-1], nutrient]
                
            data_df.loc[len(data_df)] = row



def fetchDataFromChildWebsite(link):
    response = requests.get(link)
    if response.status_code == 200:
        siteHtml = response.text
    else:
        print("Failed to retrieve "+link+" webpage")
    siteSoup = BeautifulSoup(siteHtml, 'lxml') 
    foodRecipeLinks = siteSoup.find_all('a')
    filteredRecipeLinkDataSet = {foodRecipeLink.get('href') for foodRecipeLink in foodRecipeLinks[100:120]}
    for recipeLink in filteredRecipeLinkDataSet:
        fetchDataFromRecipeWebsite(recipeLink)

def isolateDataFromMainWebsite(html):
    soup = BeautifulSoup(html, 'lxml') 
    links = soup.find_all('a')
    filtered_links = {link.get('href') for link in links if 'recipe' in link.get('href') 
                    and any(keyword in link.get('href') for keyword in ('breakfast', 'lunch', 'dinner'))}
    for link in filtered_links:
        fetchDataFromChildWebsite(link)

def main(fo_path):
    global data_df
    response = requests.get("https://ultimatepaleoguide.com/")
    if response.status_code == 200:
        html = response.text
    else:
        print("Failed to retrieve webpage")
        exit()
    isolateDataFromMainWebsite(html)
    dcw.writecsv(data_df, fo_path, 'a')