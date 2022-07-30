import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title(" My Parents New Healthy Diner")
streamlit.header(" Breakfast Menu")
streamlit.text("🥣 Omega 3 & Bluerry Oatmeal")
streamlit.text("🥗 Kale, Spinach & Rocket Smoothie")
streamlit.text("🐔 Hard-Boiled & Free-Range Egg")
streamlit.text("🥑🍞 Avocado Toast")
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def get_fruityvice(this_fruit_choice):
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
        fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
        return fruityvice_normalized

def get_fruit_load_list():
        with my_cnx.cursor() as my_cur:
                my_cur.execute("select * from fruit_load_list")
                return my_cur.featchall()
        
streamlit.header("Fruityvice Fruit Advice!")

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + 'kiwi')
# streamlit.text(fruityvice_response.json())

try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information")
    else:
#         get_fruityvice(fruit_choice)
#         fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#         fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
#         streamlit.dataframe(fruityvice_normalized)
        streamlit.dataframe(get_fruityvice(fruit_choice))
except URLError as e:
    streamlit.error()
      
#     streamlit.write('The user entered ', fruit_choice)

# fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
# streamlit.text(fruityvice_response.json())

# # write your own comment -what does the next line do? 
# fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# # write your own comment - what does this do?
# streamlit.dataframe(fruityvice_normalized)

if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)
        
# my_cur = my_cnx.cursor()
# my_cur.execute("SELECT * from pc_rivery_db.public.fruit_load_list")
# my_data_row = my_cur.fetchall()
# streamlit.header("Fruit load list contains:")
# streamlit.dataframe(my_data_row)

fruit_choice = streamlit.text_input('What fruit would you like ito add?','jackfruit')
streamlit.write('Thanks for adding ', fruit_choice)

my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('fruit_choice')")
