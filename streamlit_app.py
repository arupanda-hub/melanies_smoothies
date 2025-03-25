# docs.streamlit.io

# • :page_with_curl: [Streamlit open source documentation](https://docs.streamlit.io)
# • :snow: [Streamlit in Snowflake documentation](https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit) 
# • :books: [Demo repo with templates](https://github.com/Snowflake-Labs/snowflake-demo-streamlit)
# • :memo: [Streamlit in Snowflake release notes](https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake)

# Create Your Smoothie Order Form SIS App

# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

helpful_links = [
    "https://docs.streamlit.io",
    "https://docs.snowflake.com/en/developer-guide/streamlit/about-streamlit",
    "https://github.com/Snowflake-Labs/snowflake-demo-streamlit",
    "https://docs.snowflake.com/en/release-notes/streamlit-in-snowflake"
]

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")
st.write(
    f"""Choose the fruits you want in your custom Smoothie!"""
)

#  Adding TextBox element
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name of your Smoothie will be:", name_on_order)


#  Adding Interactive Elements

# Let's begin by adding a select box. We'll get a sample snippet from the Streamlit Input Widget SELECTBOX documentation page.  
# https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox


# Add a select box 
# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches")
# )

# st.write("Your favorite fruit is:", option)

# To remove the select box, I just commented the above section of the script


# Now Focus on the FRUIT_NAME Column
# -------------------------------
# To use a Snowpark COLUMN function named "col" we need to import it into our app. 
# We'll place the import statement close to where we plan to use it.

# from snowflake.snowpark.functions import col  -->> moved this import statement at the top near to other import statements



# Display the Fruit Options List from the database table in Your Streamlit in Snowflake (SiS) App . 
# session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

# my_dataframe = session.table("smoothies.public.fruit_options")
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()



# Add a Multiselect 
# -----------------
ingredients_list = st.multiselect('Choose up to 5 ingredients:', my_dataframe, max_selections=5)

# The Data Returned is both a list and a LIST
# ------------------------------------------
# We are placing the multiselect entries into a variable called "ingredients." We can then write "ingredients" back out to the screen.
# Our ingredients variable is an object or data type called a LIST
# A LIST is different than a DATAFRAME which is also different from a STRING!

# Display the LIST
# --------------------
# st.write(ingredients_list)
# st.text(ingredients_list)

# Cleaning Up Empty Brackets because If ingredients have not yet been chosen, then there is no need to display these. Otherwise it will show empty brackets
# --------------------------
# use if  condition
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    

#Create a Place to Store Order Data
# ----------------------------------

# Nothing to do anything in this streamlit app for this. Instead do the below steps in snowflake
# Create a table in your SMOOTHIES database.
# Make sure it is owned by SYSADMIN. 
# Name it ORDERS.
# Give it a single 200 character-limit text column named INGREDIENTS. 


# Converting a LIST to a STRING 
# -----------------------------
    ingredients_string = ''

    # To convert the LIST to a STRING we can add a FOR LOOP block. A FOR LOOP will repeat once FOR every value in the LIST. 

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '   
        st.subheader(fruit_chosen + ' Nutrition Information')   
        smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + fruit_chosen)
        # st.text(smoothiefroot_response.json())
        smoothiefroot_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width = True)


    # st.write(ingredients_string)

# Build a SQL Insert Statement & Test It
# --------------------------------------
   
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    # st.write(my_insert_stmt)
    # st.stop()


# Insert the Order into Snowflake
# -------------------------------

    # if ingredients_string:
    #     session.sql(my_insert_stmt).collect()
        
    #     st.success('Your Smoothie is ordered!', icon="✅")

# After submitting a new order, check the Snowflake table to see if the order arrived in the table in worksheet
# Then Truncate the Orders Table in worksheet

# Add a Submit Button
# -------------------
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered,' + name_on_order +'!', icon="✅")



