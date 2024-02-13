# -*- coding: utf-8 -*-
"""
Created on Sat Oct  7 19:42:22 2023

@author: 
1. Aditya Jyotindra Deshmukh - (ajdeshmu)
2. Meet Patel - (mppatel)
3. Pratyush Jain - (pratyusj)
4. Riddhima Singh - (riddhims)

"""
import pandas as pd

def initialize_df():
    df = pd.DataFrame(columns = ['Title','Link','Servings','Time to Cook',
                                  'Meal Type','Review','Ingredient',
                                  'Instructions','Nutrient Info'])
    
    return df

def writecsv(df, fo_path, mode):
    header = ['Title','Link','Servings','Time to Cook','Meal Type','Review',
              'Ingredient','Instructions','Nutrient Info']
    
    if mode=='w':
        df.to_csv(fo_path, mode=mode, index=False, header=header)
    else:
        df.to_csv(fo_path, mode=mode, index=False, header=False)