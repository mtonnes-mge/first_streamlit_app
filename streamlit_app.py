import streamlit
import pandas
import requests

streamlit.title('My parents new healthy diner')

streamlit.header('Menu')
streamlit.text('foo')
streamlit.text('bar')
streamlit.text('baz')

streamlit.header('Contact')
streamlit.text('ping v1')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# pick fruits
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selection = streamlit.multiselect("Pick your poisons", list(my_fruit_list.index), ['Banana', 'Kiwifruit'])
fruits_selected = my_fruit_list.loc[fruits_selection]

# display list
streamlit.dataframe(fruits_selected)

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
streamlit.header("Fruityvice Fruit Advice!")
streamlit.text(fruityvice_response.json())

# normalize
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
streamlit.dataframe(fruityvice_normalized)
