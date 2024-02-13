# -*- coding: utf-8 -*-
"""
Spyder Editor

@author: 
1. Aditya Jyotindra Deshmukh - (ajdeshmu)
2. Meet Patel - (mppatel)
3. Pratyush Jain - (pratyusj)
4. Riddhima Singh - (riddhims)
"""

import requests
from bs4 import Tag, BeautifulSoup
import df_csv_writer as dcw

def get_recipe(main_urlpath, fo_path, mealtype, mode):
    result = requests.get(main_urlpath)
    content = result.text
    soup = BeautifulSoup(content, 'lxml')

    box = soup.find('div', id="mntl-taxonomysc-article-list-group_1-0")
    titles = [title_tag.get_text() for title_tag in box.find_all('span', class_= "card__title-text")]
    links = [link['href'] for link in box.find_all('a', href=True)]

    df = dcw.initialize_df()
    df = get_recipe_details(titles,links, df, mealtype)
    dcw.writecsv(df, fo_path, mode)

def get_recipe_details(titles, links, df, mealtype):
    for title,link in zip(titles, links):
        try:
            result = requests.get(link)
            content = result.text
            soup = BeautifulSoup(content,'lxml')
        except:
            continue
    
        #Time and Servings
        try:
            for text in soup.find('div',class_="mntl-recipe-details__content"):
                    if isinstance(text,Tag):
                        if text.find('div', class_="mntl-recipe-details__label")\
                               .get_text() == 'Servings:':
                            servings = text\
                                       .find('div', class_="mntl-recipe-details__value")\
                                       .get_text().lower()\
                                       .replace('servings','')\
                                       .replace('serving','').strip()
                    
                        elif text.find('div', class_="mntl-recipe-details__label")\
                                 .get_text() == 'Total Time:':
                            cooktime = text\
                                       .find('div', class_="mntl-recipe-details__value")\
                                       .get_text().strip()
             
            hr_mins, mins = 0, 0
            cooktime_parts = cooktime.split(' ')
            if 'hr' in cooktime_parts:
                hr_mins = int(cooktime_parts[cooktime_parts.index('hr') - 1]) * 60
            elif 'hrs' in cooktime_parts:
                hr_mins = int(cooktime_parts[cooktime_parts.index('hrs') - 1]) * 60
            elif 'min' in cooktime_parts:
                mins = int(cooktime_parts[cooktime_parts.index('min') - 1])
            elif 'mins' in cooktime_parts:
                mins = int(cooktime_parts[cooktime_parts.index('mins') - 1])
                        
            cooktime = hr_mins + mins
                    
        except:
            continue
        
        #Reviews        
        try:
            review = soup.find('div', class_ ="comp type--squirrel-bold mntl-recipe-review-bar__rating mntl-text-block")\
                         .get_text().strip()
        except:
            review=''
        
        #Nutrient Info
        try:
            nutrient_ls = nutrient = [f'{tag.get_text()}\n' \
                                      if not tag.get_text().strip()[:-1].isnumeric()\
                                      else tag.get_text().strip() + ' ' \
                                      for tag in soup.find_all('td', class_= "mntl-nutrition-facts-summary__table-cell")\
                                     ]
            nutrient = ''.join(nutrient_ls)
        except:
            nutrient = ''
            
        #Ingredients
        try:
            ingredients = ''
            for text in soup.find_all('li', class_ ="mntl-structured-ingredients__list-item"):
                quantity = ''; unit = ''; name = '';
                
                for span in text.find_all('span'):
                    if str(span)[22:30] == 'quantity':
                        quantity = span.get_text().strip()
                    elif str(span)[22:26] == 'unit':
                        unit = span.get_text().strip()
                    elif str(span)[22:26] == 'name':
                        name = span.get_text().strip()
                
                ingredients += f'{quantity} {unit} {name}\n'
                
        except:
            continue
        
        #Instructions
        try:
            instructions = ''
            for step in soup.find_all('p',class_="comp mntl-sc-block mntl-sc-block-html"):
                instructions += f'{step.get_text().strip()}\n\n'
                
        except:
            continue
            
        
        row = [title,link,servings,cooktime,mealtype,review,\
               ingredients[:-1],instructions[:-1], nutrient]
        
        df.loc[len(df)] = row
    return df