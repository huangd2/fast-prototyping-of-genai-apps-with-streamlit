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
    # Get the current script directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # Construct the path to the CSV file
    csv_path = os.path.join(current_dir, "..", "..", "data", "customer_reviews.csv")
    return csv_path


st.title("Hello, GenAI!")
st.write("This is your GenAI-powered data processing app.")

# use st.columns to display two buttons side by side, then place a button in each of the columns
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
# Now, it would be nice to display this data set. Use this code in the bottom of the script to do it. But pay attention to how this code is written. 
# It is within an if block. You need this if statement to check whether or not a data set has been ingested and saved to the session state. Remember, 
# every time the app is reloaded, it runs the whole script. If there is no data ingested, it cannot be displayed.
if "df" in st.session_state:

    # add a subtitle for the dropdown box, show only the selected columns
    st.subheader(" Filter by Product")
    # add a dropdown box, show only the selected items
    product = st.selectbox(
        "Choose a product", ["All Products"] + st.session_state["df"]["PRODUCT"].unique().tolist())
    st.subheader(f" Dataset Preview")

    st.dataframe(st.session_state["df"].head())

    if product != "All Products":
        filtered_df = st.session_state["df"][st.session_state["df"]["PRODUCT"] == product]
    else:
        filtered_df = st.session_state["df"]
    st.dataframe(filtered_df)

# Streamlit built-in functions: matplotlib, plotly, altair, and more
# bar_chart, turns a column of sentiment scores into a tidy bar chart, works with pandas data frames or series
# st.line_chart(), st.area_chart(), st.scatter_chart()
# df.groupby("PRODUCT")["SENTIMENT"].mean()

    st.subheader("Sentiment Score by Product")
    grouped = st.session_state["df"].groupby("PRODUCT")["SENTIMENT_SCORE"].mean()
    st.bar_chart(grouped) 

# All right, what if you're already used to Matplotlib? You can totally use it here. 
# This is perfect for histograms, scattered plots, or anything where you don't need a lot of interactivity. 
# Note that you've used the filter df variable here. So the plot will change when you select something else in the dropdown menu. 

# Matplotlib plot 
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(filtered_df["SENTIMENT_SCORE"], bins=10, color='skyblue', edgecolor='black', alpha=0.7)
    ax.set_title("Sentiment Score Distribution")
    ax.set_xlabel("Sentiment Score")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)
# If you want interaction like tooltips or zoom, Plotly is a solid choice. Plotly charts feel modern and smooth.    
# Users can hover over points, zoom in, or click for more details. And you don't have to write any extra UI code. 
# To write a Plotly chart, use that last part, use container width equals to true. Just make sure that the chart stretches to 
# fit the full width of the app

# Plotly chart
    fig = px.histogram(
        filtered_df,
        x="SENTIMENT_SCORE",
        nbins=10,
        title="Sentiment Score Distribution",
        labels={"SENTIMENT_SCORE": "Sentiment Score",
                "count": "Frequency"  },
    )
    fig.update_layout(
        xaxis_title="Sentiment Score",
        yaxis_title="Frequency",
        showlegend=False
    )
    # use container width equals to true.Just make sure that the chart stretches to fit the full width of the app.
    st.plotly_chart(fig, use_container_width=True)

# Altair is another great option, especially for statistical visualizations.
# It's a declarative library, meaning you describe what you want, and it figures out how to render it.

    chart = alt.Chart(filtered_df).mark_bar().add_selection(
        alt.selection_interval()).encode(
        alt.X("SENTIMENT_SCORE:Q", bin=alt.Bin(maxbins=10),
        title = "Sentiment Score"),
        alt.Y("count():Q", title="Frequency"),
        tooltip =["count():Q"]
    ).properties(
        width=600,
        height=400,

    )
    st.altair_chart(chart, use_container_width=True)