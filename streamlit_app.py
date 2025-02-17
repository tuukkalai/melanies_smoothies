import streamlit as st
import pandas as pd
import requests
from snowflake.snowpark.functions import col


st.title(":cup_with_straw: Customize your smoothie :cup_with_straw:")
st.write("Choose the fruits you want in your custom smoothie!")

name_on_order = st.text_input("Name on Smoothie")
st.write("Name on the Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col("fruit_name"),col("search_on"))

# Converting Snowpark dataframe to pandas
pd_df = my_dataframe.to_pandas()
st.dataframe(pf_df)
st.stop()

selected_items = st.multiselect(
    "Choose up to 5 items",
    my_dataframe,
    max_selections=5
)

ingredients_string = ''
if selected_items:
    for selected_item in selected_items:
        ingredients_string += selected_item + " "
        st.subheader(f"{selected_item} Nutrition information")
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + selected_item)
        sf_df = st.dataframe(smoothiefroot_response.json(), use_container_width = True)

    query = f"""insert into smoothies.public.orders (ingredients, name_on_order)
    values ('{ingredients_string}', '{name_on_order}')"""

    order_button = st.button("Submit order")
    if order_button:
        session.sql(query).collect()
        st.success("Your smoothie is ordered!", icon='✅')

