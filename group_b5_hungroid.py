# -*- coding: utf-8 -*-
"""
Created on Fri Oct 13 18:50:58 2023

@author: 
1. Aditya Jyotindra Deshmukh - (ajdeshmu)
2. Meet Patel - (mppatel)
3. Pratyush Jain - (pratyusj)
4. Riddhima Singh - (riddhims)

"""

from tkinter import *
from tkinter import font
from PIL import ImageTk, Image 
import time

import tkinter as tk
from tkinter import ttk, Scrollbar, Text
import pandas as pd
from datetime import datetime, timedelta
import os
import random
import ics
from ics import Event
import process as p

path = os.getcwd().replace('\\','/')

    
def main_app():
    global data
    def generate_recipe_list():
        # Get user inputs
        global data
        time = cooking_time_entry.get()
        servings = servings_entry.get()
        reviews = reviews_entry.get()
        
        # Create a filter based on user inputs
        filter_criteria = (
            (data['Time to Cook'] <= int(time) if time else True) &
            (data['Servings'] == servings if servings else True) &
            (data['Review'] >= int(reviews) if reviews else True)
        )
        
        # Apply the filter to the data
        filtered_data = data[filter_criteria]
        
        # Display the matching recipes in the listbox
        recipe_listbox.delete(0, tk.END)  # Clear previous results
        for title in filtered_data['Title']:
            recipe_listbox.insert(tk.END, title)
    # Create the main window
    def view_recipe():
        global data
        selected_indices = recipe_listbox.curselection()
        if not selected_indices:
            return

        selected_recipes = [data.loc[int(index)] for index in selected_indices]
        
        # Create a popup window to display recipe details
        popup = tk.Toplevel(root)
        popup.title("Recipe Details")
        
        text = Text(popup, wrap=tk.WORD)
        text.pack(fill=tk.BOTH, expand=True)
        
        scrollbar = Scrollbar(popup, command=text.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text.config(yscrollcommand=scrollbar.set)
        
        
        
        receipies = []
        for recipe in selected_recipes:
            receipies.append("Title: "+str(recipe['Title'])+"\n"
                             +"Servings: "+str(recipe['Servings'])+"\n"
                             +"Time to Cook: "+str(recipe['Time to Cook'])+"\n"
                             +"Meal Type: "+str(recipe['Meal Type'])+"\n"
                             +"Ingredients: "+str(recipe['Ingredient'])+"\n"
                             +"Instructions: "+str(recipe['Instructions'])+"\n"
                             +"Nutrient Info: "+str(recipe['Nutrient Info'])+"\n"
                             +"_______________________________________________\n\n"
                             )
        for i in receipies:
            text.insert(tk.END, i)
    def finalise_plan():
        global data
        selected_indices = recipe_listbox.curselection()
        if not selected_indices:
            return

        selected_recipes = [data.loc[int(index)] for index in selected_indices]

        selected_recipes_titles = []
        for recipe in selected_recipes:
            selected_recipes_titles.append(recipe['Title'])

        meal_planner_window = tk.Toplevel(root)
        meal_planner_window.title("Meal Planner")

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        meals = ["Breakfast", "Lunch", "Dinner"]

        meal_comboboxes = {}  # Store comboboxes in a dictionary
        def generate_ics():
            global data
            selections = []
            for day in days:
                day_selections = []
                for meal in meals:
                    if meal_comboboxes[day][meal].get() != '':
                        selected = meal_comboboxes[day][meal].get()
                        day_selections.append(f"{meal}: {selected}")
                selections.append(day_selections)

            # Create an .ics Calendar object
            calendar = ics.Calendar()

            # Define a start date (e.g., the upcoming week's Monday)
            start_date = datetime.now()
            while start_date.weekday() != 0:  # 0 represents Monday
                start_date += timedelta(days=1)

            # Generate events for selected recipes with descriptions
            for i, day_selection in enumerate(selections):
                for j, recipe in enumerate(day_selection):
                    event = Event()
                    event.name = f"Day {i+1}, {meals[j]}: {recipe}"
                    event.description = f"Recipe: {recipe}"
                    event.begin = start_date + timedelta(days=i, hours=j * 4)  # Assuming 4 hours per meal
                    event.end = event.begin + timedelta(hours=1)  # Assuming each meal lasts 1 hours
                    calendar.events.add(event)

            # Save the calendar to an .ics file
            with open("meal_plan.ics", "w") as f:
                f.writelines(calendar)

            print("Meal plan saved as 'meal_plan.ics'")
            
        for day in days:
            ttk.Label(meal_planner_window, text=day).grid(column=0, row=days.index(day) + 1)
            meal_comboboxes[day] = {}
            for meal in meals:
                ttk.Label(meal_planner_window, text=meal).grid(column=meals.index(meal) + 1, row=0)
                meal_comboboxes[day][meal] = ttk.Combobox(meal_planner_window, values=selected_recipes_titles)
                default_value = random.choice(selected_recipes_titles)
                meal_comboboxes[day][meal].set(default_value)
                meal_comboboxes[day][meal].grid(column=meals.index(meal) + 1, row=days.index(day) + 1)
                
        save_button = ttk.Button(meal_planner_window, text="Export Selection for calendar", command=generate_ics)
        save_button.grid(column=0, row=len(days) + 2, columnspan=len(meals) + 1)
    root = tk.Tk()
    root.title("Hungroid")

    # Create labels and entry fields
    cooking_time_label = ttk.Label(root, text="Cooking Time (minutes):")
    cooking_time_entry = ttk.Entry(root)

    servings_label = ttk.Label(root, text="Servings (optional):")
    servings_entry = ttk.Entry(root)

    reviews_label = ttk.Label(root, text="Reviews (optional):")
    reviews_entry = ttk.Entry(root)

    # Create a button to generate the recipe list
    generate_button = ttk.Button(root, text="Generate Recipe List", command=generate_recipe_list)

    # Create a listbox to display matching recipes (multi-select)
    recipe_listbox = tk.Listbox(root, selectmode=tk.MULTIPLE, width=50, height=10)
    recipe_listbox.bind("<Double-Button-1>", lambda event: view_recipe())

    # Create a label to display recipe details
    recipe_info_label = ttk.Label(root, text="", wraplength=400)

    # Create a button to generate the recipe list
    finalise_button = ttk.Button(root, text="Finalise the plan", command=finalise_plan)

    # Grid layout
    cooking_time_label.grid(row=0, column=0, padx=5, pady=5)
    cooking_time_entry.grid(row=0, column=1, padx=5, pady=5)
    servings_label.grid(row=1, column=0, padx=5, pady=5)
    servings_entry.grid(row=1, column=1, padx=5, pady=5)
    reviews_label.grid(row=2, column=0, padx=5, pady=5)
    reviews_entry.grid(row=2, column=1, padx=5, pady=5)
    generate_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
    recipe_listbox.grid(row=4, column=0, columnspan=2, padx=5, pady=5)
    recipe_info_label.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    finalise_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    # Start the main event loop
    root.mainloop()




w=Tk()
w.title("Hungroid")
#Using piece of code from old splash screen
width_of_window = 427
height_of_window = 250
screen_width = w.winfo_screenwidth()
screen_height = w.winfo_screenheight()
x_coordinate = (screen_width/2)-(width_of_window/2)
y_coordinate = (screen_height/2)-(height_of_window/2)
w.geometry("%dx%d+%d+%d" %(width_of_window,height_of_window,x_coordinate,y_coordinate))
w.configure(bg='#272727')
w.update_idletasks()

Frame(w, width=427, height=250, bg='#272727').place(x=0,y=0)

w.update_idletasks()
label1=Label(w, text='Hungroid', fg='white', bg='#272727') #decorate it 
label1.configure(font=("Game Of Squids", 24, "bold"))   #You need to install this font in your PC or try another one
label1.place(x=135,y=90)

w.update_idletasks()
label2=Label(w, text='Processing Source 1', fg='white', bg='#272727') #decorate it 
label2.configure(font=("Calibri", 11))
label2.place(x=10,y=215)
w.update_idletasks()

image_a=ImageTk.PhotoImage(Image.open('c2.png'))
image_b=ImageTk.PhotoImage(Image.open('c1.png'))

w.update_idletasks()
l1=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=180, y=145)
l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
w.update_idletasks()
p.s1()
w.update_idletasks()

w.update_idletasks()
label2.config(text="Processing Source 2")
l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
l2=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=200, y=145)
l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
w.update_idletasks()
p.s2()


w.update_idletasks()
label2.config(text="Processing Source 3")
l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
l3=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=220, y=145)
l4=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=240, y=145)
w.update_idletasks()
p.s3()



label2.config(text="Processing Source 4")
l1=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=180, y=145)
l2=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=200, y=145)
l3=Label(w, image=image_b, border=0, relief=SUNKEN).place(x=220, y=145)
l4=Label(w, image=image_a, border=0, relief=SUNKEN).place(x=240, y=145)
w.update_idletasks()
p.s4()


w.destroy()
data = pd.read_csv(f'{path}/recipes_data.csv')
main_app()
w.mainloop()