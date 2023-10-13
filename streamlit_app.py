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
streamlit.header("Fruityvice Fruit Advice!")
try:
  fruit_choice = streamlit.text_input('What fruit do you want info about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get info about.")
  else:
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    # normalize
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
    streamlit.error()

streamlit.stop()

### Snowflake FRUIT LIST ###
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

streamlit.text("Hellow from snowflake:")
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text(my_data_row)

streamlit.text("Snowflake context:")
my_cur.execute("select current_database(), current_schema()")
my_data_row = my_cur.fetchone()
streamlit.text(my_data_row)

streamlit.text("The fruit list:")
my_cur.execute("select * from FRUIT_LOAD_LIST")
# my_data_row = my_cur.fetchone()
# streamlit.text(my_data_row)
my_data_rows = my_cur.fetchall()
streamlit.dataframe(my_data_rows)

new_fruit = streamlit.text_input('Add another fruit:')
my_cur.execute("INSERT INTO FRUIT_LOAD_LIST (FRUIT_NAME) VALUES ('"+new_fruit+"')") # great sql injection
streamlit.write('You added ', new_fruit)
