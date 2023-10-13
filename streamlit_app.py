import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents new healthy diner')

streamlit.header('Menu')
streamlit.text('foo')
streamlit.text('bar')
streamlit.text('baz')

streamlit.header('Contact')
streamlit.text('ping v2')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# pick fruits
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selection = streamlit.multiselect("Pick your poisons", list(my_fruit_list.index), ['Banana', 'Kiwifruit'])
fruits_selected = my_fruit_list.loc[fruits_selection]

# display list
streamlit.dataframe(fruits_selected)

########## Fruityvice
def get_fruityvice_data(fruit):
  fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit)
  fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
  return fruityvice_normalized

streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit do you want info about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get info about.")
  else:
    streamlit.dataframe(get_fruityvice_data(fruit_choice))

except URLError as e:
    streamlit.error()

### Snowflake FRUIT LIST ###
def get_fruit_load_list():
  with my_cnx.cursor() as my_cur:
    my_cur.execute("select * from fruit_load_list")
    return my_cur.fetchall()

if streamlit.button("Get fruit load list"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  streamlit.dataframe(get_fruit_load_list())

# input fruit
def insert_fruit(fruit):
  with my_cnx.cursor() as my_cur:
    my_cur.execute("INSERT INTO FRUIT_LOAD_LIST (FRUIT_NAME) VALUES ('"+new_fruit+"')") # great sql injection

fruit_to_add = streamlit.text_input('Add another fruit:')
if streamlit.button("Add fruit!"):
  my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
  insert_fruit(fruit_to_add)
  streamlit.write('You added ', fruit_to_add)
