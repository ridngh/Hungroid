
"""
Created on Fri Oct 13 18:50:58 2023

@author: 
1. Aditya Jyotindra Deshmukh - (ajdeshmu)
2. Meet Patel - (mppatel)
3. Pratyush Jain - (pratyusj)
4. Riddhima Singh - (riddhims)
"""



import requests
import pandas as pd
import df_csv_writer as dcw

def fetch_data(fo_path):
    # Airtable base ID and table name
    BASE_ID = 'appuDSkKssseYbWca'
    TABLE_NAME = 'Recipes'
    
    # (Personal Access Token)
    personal_access_token=""
    
    # Airtable API endpoint
    url = f'https://api.airtable.com/v0/{BASE_ID}/{TABLE_NAME}'
    
    # Headers with API key
    headers = {
        'Authorization': f'Bearer {personal_access_token}',
    }
    
    # Making GET request to Airtable
    response = requests.get(url, headers=headers)
    
    # Check if the request was successful, else give failure
    if response.status_code == 200:
        data = response.json()
        records = data.get('records', [])
        
        # Create a list of dictionaries for the records
        records_data = []
        for record in records:
            fields = record.get('fields', {})
            records_data.append(fields)
        
        # Convert the list of dictionaries to a DataFrame
        df = pd.DataFrame(records_data)
    
        # try:
            # df.to_csv('testdata.csv')
        # except:
            # print("CSV ISSUES!")
        
        # Now 'df' contains our data, sorting with our columns_of_interest
        columns_of_interest = ['Name','Link', 'Prep Time', 'Type', 'Ingredients']
        df = df[columns_of_interest]
        df = df.rename(columns={'Name': 'Title','Prep Time': 'Time to Cook', 'Type':'Meal Type'})
        df = df.dropna(subset=['Link'])
        df = df[df['Meal Type'] == 'Main Dish']
        
        pd.options.mode.chained_assignment = None
        df.index = range(34)
        for (i,j) in zip(range(17),range(17,34)):
            df['Meal Type'].loc[i] = 'Lunch'
            df['Meal Type'].loc[j] = 'Dinner'
        
        for i in range(len(df)):
            df["Ingredients"].loc[i] = '\n'.join(df["Ingredients"].loc[i])
            
            
        df["Instructions"] = "Please visit the given link for complete ingredients and instructions."
        df.insert(loc = 2,
              column = 'Servings',
              value = '')
        df.insert(loc = 5,
              column = 'Review',
              value = '')
        df["Nutrient Info"] = ''
        
        dcw.writecsv(df, fo_path, 'a')
    
    
    
    else:
        print(f"Failed to retrieve data. Status code: {response.status_code}")
        print(response.text)
