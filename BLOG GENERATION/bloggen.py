import streamlit as st
import requests

# Set Cohere API key directly in the code (temporary approach)
cohere_api_key = "e6Grqw2QPaETzGsVztx7wR827YrLT13vhCqZGc1e"  # Replace with your actual Cohere API key

# Function to get response from Cohere's API
def get_blog_response(input_text, no_words, blog_style):
    url = "https://api.cohere.ai/generate"
    
    headers = {
        "Authorization": f"Bearer {cohere_api_key}",
        "Content-Type": "application/json"
    }
    
    # Prepare the prompt
    prompt = f"Write a blog for {blog_style} job profile on the topic '{input_text}' within {no_words} words."
    
    # Prepare the data for the API request
    data = {
        "model": "command",  # Specify the model you want to use
        "prompt": prompt,
        "max_tokens": int(no_words),  # Limit the response to the specified number of words
        "temperature": 0.7,  # Control the creativity of the response
        "stop_sequences": ["\n"]  # Optionally define stop sequences
    }
    
    try:
        # Send the request to Cohere's API
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Extract the response JSON
            response_data = response.json()
            
            # Return the generated text
            return response_data.get('text', 'No response generated.')
        else:
            return f"Error: {response.status_code} - {response.text}"
    
    except Exception as e:
        return f"Error: {str(e)}"

# Initialize Streamlit app
st.set_page_config(page_title="Generate Blogs", page_icon='🤖', layout='centered', initial_sidebar_state='collapsed')

st.header("Generate Blogs 🤖")

# User input
input_text = st.text_input("Enter the Blog Topic")

# Creating two more columns for additional fields
col1, col2 = st.columns([5, 5])

with col1:
    no_words = st.text_input('No of Words')
with col2:
    blog_style = st.selectbox('Writing the blog for', ('Researchers', 'Data Scientist', 'Common People'), index=0)

# Button to trigger the blog generation
submit = st.button("Generate")

# Final response
if submit:
    if input_text and no_words:
        st.write(get_blog_response(input_text, no_words, blog_style))
    else:
        st.write("Please fill in all the fields.")
