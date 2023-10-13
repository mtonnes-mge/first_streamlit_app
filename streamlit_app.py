import streamlit
import pandas
import requests
import snowflake.connector

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

fruit_choice = streamlit.text_input('What fruit do you want info about?', 'Kiwi')
streamlit.write('You chose', fruit_choice)
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

# normalize
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hellow from snowflake:")
streamlit.text(my_data_row)

my_cur.execute("select current_database(), current_schema()")
my_data_row = my_cur.fetchone()
streamlit.text("Snowflake context:")
streamlit.text(my_data_row)

my_cur.execute("select * from PC_RIVERY_DB.PUBLIC.fruit_load_list")
my_data_row = my_cur.fetchone()
streamlist.text("The fruit list:")
streamlist.text(my_data_row)

