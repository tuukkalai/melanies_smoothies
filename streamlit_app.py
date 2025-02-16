# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberry", "Peach"),
# )

# st.write("You selected:", option)

name_on_order = st.text_input("Name on Smoothie")
st.write("Name on the Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"))
# st.dataframe(data=my_dataframe, use_container_width=True)

selected_items = st.multiselect(
    "Choose up to 5 items",
    my_dataframe,
    max_selections=5
)

ingredients_string = ''
if selected_items:
    # st.write(selected_items)
    for selected_item in selected_items:
        ingredients_string += selected_item + " "
    query = """insert into smoothies.public.orders (ingredients, name_on_order)
    values ('""" + ingredients_string + """', '""" + name_on_order + """')"""
    # st.write(query)
    
    order_button = st.button("Submit order")
    if order_button:
        session.sql(query).collect()
        st.success("Your smoothie is ordered!", icon='✅')

smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response.json())
