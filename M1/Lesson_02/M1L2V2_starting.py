# import packages
from dotenv import load_dotenv
import openai
import streamlit as st


@st.cache_data
# move the model call to its own function named get_response.
# then put the decorator on top of the getResponse function like this. st.cache data is a Streamlit decorator that improves app speed by caching the results 
# of a previous function or calculation. It tells Streamlit, I've seen this input before. Just return the cached result instead of re-running the code. 
# It's especially useful with genAI apps because genAI calls take time and cost money. So if you ask the model to analyze the same data set again and again, 
# you can use st.cache data to get the result instantly. Instead of hitting the API again and again. In the Avalanche project, this is something you might 
# want to consider using for any data transforms you need to do.
def get_response(user_prompt, temperature):
    response = client.responses.create( # used to send your msg to an OpenAI model and return its response
        model = "gpt-4o",
        input = [ # a list that keeps track of your conversation history as a list.
        {"role": "user", "content": user_prompt} # it stores the role that the model took when generating a response and the actual response itself. prompt
        ],
        temperature = temperature, # temperature controls how creative the AI is. 0.0 means very predictable. 1.0 means very creative (might be prone to incorrect responses). A bit of creativity
        max_output_tokens = 100 # limit response length, can help control costs and make answers more or less detailed.

        )
    return response


# load environment variables from .env file
load_dotenv() # grab everything from .env file and store it as environment variable in your scripts 

# initialize OpenAI client
client = openai.OpenAI() # used to retrieve OpenAI API key loaded with load_dotenv func, then it creates a connection to the OpenAI client API

st.title("Hello, GenAI") # creates a large heading for the app
st.write("This is your first Streamlit app.") # st.write is a flexible func that can display text, numbers, df, and more

# Add a text input box for user prompt
user_prompt = st.text_input("Enter your prompt:", "Explain generative AI in one sentence.") # default prompt to populate the box "Explain gen..."

# Add a slider for temperature
temperature = st.slider(
    "Model temperature:",
    min_value = 0.0,
    max_value = 1.0,
    value = 0.7, # default value
    step = 0.01,
    help = "Controls randowmness: 0 = deterministic, 1 = very creative"
)

# add a spinner that gives your users a visualization letting them know the model is running the API call. Wrap the API call code in a with st.spinner block.
# If you're calling the model multiple times with the same input especially during development, you can cache the results using the st.cache data decorator.
# It's basically a wrapper much like a with statement that you can put around a function to change or enhance what it does without modifying the original function. 
# So the first thing you need to do is move the model call to its own function named get_response. The app should work exactly the same.
with st.spinner("AI is working..."):
    # update the model call down here in the specific field (user_prompt, temperature)
    response = get_response(user_prompt, temperature)

# print the response from OpenAI
st.write(response.output[0].content[0].text) # display the output of the model in the app

# st.text_input(): text box for prompts
# st.button(): triggers action
# st.selectbox(): adds drop-downs for model selectin
# st.slider(): adjusts values like temperatures
# st.checkbox(): creates on-off toggles
# st.file_uploader(): uploades CSVs or text files
# st.spinner(): shows a loading animation when waiting for something


