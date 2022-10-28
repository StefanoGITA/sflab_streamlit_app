import streamlit
import pandas as pd
import requests


streamlit.title(" My parents new healthy Diner")

streamlit.header("Breakfast Favorites")
streamlit.text("🥣 Omega 3 & Blueberry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled Free-Range Eggs")
streamlit.text("🥑🍞 Avocado Toast")

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Banana', 'Pineapple'])
streamlit.text(fruits_selected)
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
data = []
for fruit_name in fruits_selected:
    response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_name}")
    # pd.json_normalize convert a json to dataframe
    # d = json_normalize(response.json()
    data.append(response.json())

streamlit.text(data)
# Convert a json to dataframe
# Put the dataframe in streamlit
# streamlit.dataframe(data)
