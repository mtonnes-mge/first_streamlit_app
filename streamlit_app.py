import streamlit
import pandas

streamlit.title('My parents new healthy diner')

streamlit.header('Menu')
streamlit.text('foo')
streamlit.text('bar')
streamlit.text('baz')

streamlit.header('Contact')
streamlit.text('ping')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# pick fruits
streamlit.multiselect("Pick your poisons", list(my_fruit_list.index))

# display list
streamlit.dataframe(my_fruit_list)
