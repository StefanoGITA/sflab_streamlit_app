import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError


def get_fruit_load_list(cnx):
    with cnx.cursor() as my_cur:
        # my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
        my_cur.execute("SELECT * from fruit_load_list order by 1")
        return my_cur.fetchall()


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
try:
    fruit_name = streamlit.text_input('What fruit would you like information about?')
    if not fruit_name:
        streamlit.error("Please select a fruit to get information.")
    else:
        response = requests.get(f"https://fruityvice.com/api/fruit/{fruit_name}")
        # pd.json_normalize convert a json to dataframe
        streamlit.dataframe(pd.json_normalize(response.json()))
except URLError as e:
    streamlit.error(str(e))

streamlit.header("The fruit load list contains:")
if streamlit.button("Get Fruit Load List"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list(my_cnx)
    streamlit.dataframe(my_data_rows)


# add_my_fruit = streamlit.text_input('What fruit would you like to add?')
# if add_my_fruit:
#     streamlit.write('thanks for adding', add_my_fruit)
#     my_cur.execute(f"insert into fruit_load_list values('{add_my_fruit}')")
