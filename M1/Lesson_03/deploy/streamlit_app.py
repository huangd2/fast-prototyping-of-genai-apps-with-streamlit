# import packages
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt
import string
import re
import os

def clean_text(text):
    """
    Cleans the input text by removing punctuation, converting to lowercase, and stripping whitespace.
    """
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Convert to lowercase
    text = text.lower()
    # Strip leading and trailing whitespace
    text = text.strip()
    return text


# Helper function to get dataset path
def get_dataset_path():
    # Go up from the current file to the project root
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
    # Construct the path to the CSV in the top-level data folder
    csv_path = os.path.join(project_root, "data", "customer_reviews.csv")
    return csv_path


st.title("Hello, GenAI!")
st.write("This is your GenAI-powered data processing app.")

# Layout two buttons side by side
col1, col2 = st.columns(2)

with col1:
    if st.button("📥 Ingest Dataset"):
        # pass
        try:
            csv_path = get_dataset_path()
            # An important thing you should notice here is that the data frame was not simply saved to a df variable as usually done, 
            # but to something called a session state. The reason you need to do this is that Streamlit reruns the entire script from 
            # top to bottom. Every time the user interacts with the app. This means that if you click a button, all the variables are lost. 
            # Unless you store them somewhere that's persistent between runs. To achieve this, you can use something called session state.
            # By storing the data frame in st.session_state df, your app remembers it even if the script runs again. This allows the user 
            # to ingest the data set that later perform operations on it without the need to ingest it again. 
            st.session_state["df"] = pd.read_csv(csv_path)
            st.success("Dataset loaded successfully!")
        except FileNotFoundError:
            st.error("Dataset not found. Please check the file path.")

with col2:
    if st.button("🧹 Parse Reviews"):
        if "df" in st.session_state:
            st.session_state["df"]["CLEANED_SUMMARY "] = st.session_state["df"]["SUMMARY"].apply(clean_text)
            st.success("Reviews parsed and cleaned!")
        else:
            st.warning("Please ingest the dataset first.")

# Display the dataset if it exists
if "df" in st.session_state:
    # Product filter dropdown
    st.subheader("🔍 Filter by Product")
    product = st.selectbox("Choose a product", ["All Products"] + list(st.session_state["df"]["PRODUCT"].unique()))
    st.subheader(f"📁 Reviews for {product}")

    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)
    
    st.subheader("Sentiment Score by Product")
    grouped = st.session_state["df"].groupby(["PRODUCT"])["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped)
