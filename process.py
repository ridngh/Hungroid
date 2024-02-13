# -*- coding: utf-8 -*-
"""
Created on Fri Oct  6 15:40:47 2023

@author: @author: 

1. Aditya Jyotindra Deshmukh - (ajdeshmu)
2. Meet Patel - (mppatel)
3. Pratyush Jain - (pratyusj)
4. Riddhima Singh - (riddhims)
"""

import web_all_recipes as war
import os
import txt_mastercook as tmc
import baseFilePaleo as bfp
import token_airtable as tat
    
path = os.getcwd().replace('\\','/')
fo_path = f'{path}/recipes_data.csv'
    
    
def s1():
    global fo_path
    print("Processing Started")
    website_ar_breakfast = 'https://www.allrecipes.com/recipes/78/breakfast-and-brunch/'
    website_ar_lunch = 'https://www.allrecipes.com/recipes/17561/lunch/'
    website_ar_dinner = 'https://www.allrecipes.com/recipes/17562/dinner/'
    war.get_recipe(website_ar_breakfast, fo_path, 'Breakfast', 'w')
    print('AllRecipes Breakfast Done')
    
    war.get_recipe(website_ar_lunch, fo_path, 'Lunch', 'a')
    print('AllRecipes Lunch Done')
    
    war.get_recipe(website_ar_dinner, fo_path, 'Dinner', 'a')
    print('AllRecipes Dinner Done')
    
def s2():    
    txt_mc_breakfast = 'https://mc6help.tripod.com/RecipeLibrary/AllBreakfastRecipes.txt'
    tmc.get_recipe(txt_mc_breakfast, fo_path, 'Breakfast', 'a' )
    print('Mastercook Breakfast Done')
    
def s3():
    bfp.main(fo_path)
    print('Paleo Done')

def s4():
    tat.fetch_data(fo_path)
    print('Air Table Done')