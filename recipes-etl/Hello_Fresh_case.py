# coding: utf-8

import json
import pandas as pd
import isodate
from Levenshtein import distance

file_path = "recipes.json"


# ### Find each receipt that has “Chilies”

# Function to check if a word is similar to the target word ("Chilies")
def is_similar(word, target_word, threshold=2):
    return distance(word.lower(), target_word.lower()) <= threshold


# List to store recipes containing "Chilies"
chilies_recipes = []

with open(file_path, "r") as file:
       for line in file:
            try:
                # Load the JSON data from the line
                recipe = json.loads(line)
                for word in recipe["ingredients"].split(): ##split string into words
                    if is_similar(word, "Chilies"):
                        json_object = {"name": recipe['name'],"cookTime": recipe['cookTime'],
                                       "prepTime": recipe['prepTime'],"word": word}
                        chilies_recipes.append(json_object)
                        break  # Stop checking ingredients once a match is found
                    
            except json.JSONDecodeError as e:
                # Handle invalid JSON data
                print(f"Error decoding JSON: {e}")    
df = pd.DataFrame(chilies_recipes)
print(df["word"].unique()) ###checking the correctness of the found words
df_filtered = df[~df["word"].str.lower().isin(["chives", "chilled"])] ###deleting erroneously found ones
print(df_filtered["word"].unique())
df_filtered


# ### Add an extra field to each of the extracted recipes with the name difficulty.


def duration_to_minutes(duration_str):
    if not duration_str:  # If the string is empty return None
        return None  
    else:
        duration = isodate.parse_duration(duration_str)
        return int(duration.total_seconds() / 60)

def calculate_difficulty(row):
    ##To handle the empty strings
    prep_duration = isodate.parse_duration(row["prepTime"]).total_seconds() / 60 if row["prepTime"] else None
    cook_duration = isodate.parse_duration(row["cookTime"]).total_seconds() / 60 if row["cookTime"] else None
 ##return "Unknown" if at least one of times is missing
    if prep_duration is None or cook_duration is None:
        return "Unknown"
    
    total_duration = prep_duration + cook_duration
    
    if total_duration > 60:
        return "Hard"
    elif 30 <= total_duration <= 60:
        return "Medium"
    else:
        return "Easy"

df_filtered["difficulty"] = df_filtered.apply(calculate_difficulty, axis=1) # Apply the function to each row of the DataFrame
df_filtered.drop(['cookTime','prepTime','word'], axis=1, inplace=True) ##drop unnecessary columns
df_filtered

df_filtered.to_csv('recipes_with_time.csv', index=None,
                        encoding="utf-8-sig") ##set dataframe as csv file


