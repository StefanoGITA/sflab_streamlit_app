import streamlit
import pandas as pd
import requests
import snowflake.connector


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
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

streamlit.header("Fruityvice Fruit Advice!")
fruit_name = streamlit.text_input('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered ', fruit_name)
response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_name}")
# pd.json_normalize convert a json to dataframe
streamlit.dataframe(pd.json_normalize(response.json()))

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
# my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_cur.execute("SELECT * from fruit_load_list")
my_data_row = my_cur.fetchone()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

# d = pd.DataFrame()
# for fruit_name in fruits_selected:
#     response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_name}")
#     # pd.json_normalize convert a json to dataframe
#     row = pd.json_normalize(response.json())
#     if d.empty:
#         d = pd.DataFrame(row)
#     else:
#         d = d.append(row)
# streamlit.dataframe(d)
