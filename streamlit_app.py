import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents new healthy Diner')
streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 and Blueberry oatmeal')
streamlit.text('Kale, Spinach &  Rocket Smoothie')
streamlit.text('Hard-Bolied Free-Range Egg')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
#streamlit.dataframe(my_fruit_list)
streamlit.dataframe(fruits_to_show)

#import requests
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+fruit_choice)
    # Takes the json response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    # Output to the screen as table
    return fruityvice_normalized
      
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.header("Fruityvice Fruit Advice!")
#streamlit.text(fruityvice_response.json())
try:
   fruit_choice = streamlit.text_input('Which fruit would you like information about?')
   if not fruit_choice:
    streamlit.error('Please select fruit choice to get information.')
   else: 
    streamlit.write('The user entered ',fruit_choice)
    back_from_function = get_fruityvice_data(fruit_choice)
    streamlit.dataframe(back_from_function)
    
except URLError as e:
  streamlit.error()

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select fruit_name from pc_rivery_db.public.fruit_load_list")
        return my_cur.fetchall()
    
# import snowflake.connector
if streamlit.button('Get Fruit List'):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  my_data_rows = get_fruit_load_list()
  streamlit.header("View our Fruit List - Add your Favourites:")
  streamlit.dataframe(my_data_rows)
  #streamlit.text(my_data_rows)  
  my_cnx.close()  

# my_cur.execute("insert into fruit_load_list values ('from streamlit new_fruit variable)'")    
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into pc_rivery_db.public.fruit_load_list values ('"+ new_fruit +"')")
        return "Thanks for adding " + new_fruit
    
add_my_fruit=streamlit.text_input('Which fruit would you like to add?','Kiwi')
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx.close()
    #streamlit.write('Thanks for adding ',add_my_fruit)
    streamlit.text(back_from_function)
    
