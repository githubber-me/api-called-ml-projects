import streamlit as st
import requests

# Set your Cohere API key here (replace with your actual key)
cohere_api_key = "e6Grqw2QPaETzGsVztx7wR827YrLT13vhCqZGc1e"  # Replace with your actual Cohere API key

# Function to get summary from Cohere API
def summarize_text(input_text, summary_length):
    url = "https://api.cohere.ai/generate"
    
    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare the prompt for summarization
    prompt = f"Summarize the following text in {summary_length} sentences: {input_text}"
    
    # Prepare the data for the API request
    data = {
        "model": "command",  # Specify the model you want to use
        "prompt": prompt,
        "max_tokens": 200,  # Maximum number of tokens in the response (to control summary length)
        "temperature": 0.5,  # Control the creativity of the summary
        "stop_sequences": ["\n"]  # Optional stop sequence
    }
    
    try:
        # Send the request to Cohere's API
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the response JSON
            response_data = response.json()
            
            # Return the generated summary text
            return response_data.get('text', 'No summary generated.')
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize Streamlit app
st.set_page_config(page_title="Text Summarization", page_icon='✍️', layout='centered', initial_sidebar_state='collapsed')

st.header("Text Summarization ✍️")

# User input for the text to be summarized
input_text = st.text_area("Enter the text to summarize", height=300)

# Creating a column for summary length
summary_length = st.slider('Select summary length (in sentences)', min_value=1, max_value=5, value=2)

# Button to trigger the summarization
submit = st.button("Generate Summary")

# Final response
if submit:
    if input_text:
        st.subheader("Generated Summary:")
        st.write(summarize_text(input_text, summary_length))
    else:
        st.write("Please enter some text to summarize.")
