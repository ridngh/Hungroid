# -*- coding: utf-8 -*-
"""
Created on Sun Oct  8 20:15:20 2023

@author: 
1. Aditya Jyotindra Deshmukh - (ajdeshmu)
2. Meet Patel - (mppatel)
3. Pratyush Jain - (pratyusj)
4. Riddhima Singh - (riddhims)
"""

import requests
import df_csv_writer as dcw

def get_recipe(main_urlpath, fo_path, mealtype, mode):
    result = requests.get(main_urlpath)
    content = result.text
    recipes = []
    recipe = []
    rc = 0
    for line in content.split('\n'):
        if line[:-1] == '* Exported from MasterCook *' and not rc and not recipe:
            recipe.append(line)
        elif line[:-1] == '* Exported from MasterCook *':
            recipes.append(recipe)
            rc = rc+1
            recipe = []
            recipe.append(line)
        elif line:
            recipe.append(line)
    
    df = dcw.initialize_df()
    get_recipe_details(recipes, mealtype, df, main_urlpath)
    dcw.writecsv(df, fo_path, mode)

def get_recipe_details(recipes,mealtype, df, main_urlpath):
    for recipe in recipes:
    
        servings_index = recipe[5].find('Serving Size  : ') \
                                  + len('Serving Size  : ')                            
        servings_index_end = recipe[5].find('Preparation Time : ')
        cooktime_index = recipe[5].find('Preparation Time : ') \
                                  + len('Preparation Time : ')
                                  
        title = recipe[2].strip().replace('\n','')
        servings = recipe[5][servings_index : servings_index_end].strip()
        link = main_urlpath
        cooktime = recipe[5][cooktime_index : ].strip()  
        if cooktime == '0:00':
            cooktime = ''
        elif cooktime.find(':') != -1:
            cooktime_sep_index = cooktime.find(':')
            hr_mins = int(cooktime[0:cooktime_sep_index].strip()) * 60
            mins = int(cooktime[cooktime_sep_index + 1 :].strip())
            cooktime = hr_mins + mins
        
        ingredients = ''
        ingredient_list_start_index = 9
        for i in range(0, len(recipe) - 9):
            if recipe[ingredient_list_start_index + i] == '\r':
                ingredient_list_end_index = ingredient_list_start_index + i
                break
            
            for letter in recipe[ingredient_list_start_index + i]:
                if letter == ' ' and ingredients == '':
                    continue
                elif letter == ' ' and ingredients[-1] in (' ','\n'):
                    continue
                elif letter == '\r':
                    ingredients += '\n'
                else:
                    ingredients += letter
    
        
        instructions = ''            
        for i in range(ingredient_list_end_index + 1, len(recipe)):
            if recipe[i][:-1] in ['Source:','Description:','Yield:']:
                break # instructions over
            elif recipe[i][:5] in ['Note:', 'Makes']:
                break # instructions over
            elif recipe[i][:6] in ['Yield;']:
                break # instructions over
            elif recipe[i][:13] == 'MC Formatted':
                break # instructions over
            elif recipe[i].find('Cookbook') is True:
                break # instructions over
            elif recipe[i] == '\r' and recipe[i+1] =='\r':
                break
            
            instructions += recipe[i].replace('\r','\n')
            
        review = ''
        
        nutrient = ''
    
        row = [title,link,servings,cooktime,mealtype,review,\
           ingredients,instructions[:-1], nutrient]
    
        df.loc[len(df)] = row
    return df