import pandas as pd
import requests
import streamlit as st
# from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

order_name = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", order_name)

# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

df = session.table("smoothies.public.fruit_options").select(col("FRUIT_NAME"), col("SEARCH_ON"))
# st.dataframe(data=df, use_container_width=True)
# st.stop()

pandas_df = df.to_pandas()
# st.dataframe(pandas_df)
# st.stop()

# st.dataframe(data=df, use_container_width=True)

ingredients = st.multiselect(
    "Choose up to 5 ingredients:",
    df,
    max_selections=5,
)

# r = requests.get("https://fruityvice.com/api/fruit/watermelon")
# fv_df = st.dataframe(data=r.json(), use_container_width=True)

if ingredients: 
    
    # st.write(ingredients)
    # st.text(ingredients)
    
    # ingredient_str = " ".join(ingredients)

    ingredient_str = ""
    
    for ingredient in ingredients:

        ingredient_str += ingredient + " "
        
        search_on=pandas_df.loc[pandas_df['FRUIT_NAME'] == ingredient, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', ingredient,' is ', search_on, '.')
        
        st.subheader(f"{ingredient} Nutrition Information")
        r = requests.get(f"https://fruityvice.com/api/fruit/{search_on}")
        fv_df = st.dataframe(data=r.json(), use_container_width=True)
    
    # st.write(ingredient_str)

    insert = """insert into smoothies.public.orders(ingredients, name_on_order)
                values ('""" + ingredient_str + """','""" + order_name + """')"""

    submit = st.button("Submit Order")
    
    if submit:
        session.sql(insert).collect()

        st.success("Your Smoothie is ordered, " + order_name + "!", icon="✅")
