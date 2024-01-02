# Import necessary libraries
import os
import streamlit as st
import google.generativeai as genai 
from dotenv import load_dotenv
from PIL import Image

# Load environment variables from .env file
load_dotenv()

# Get the Google API key from the environment variables
api_key = os.getenv("GOOGLE_API_KEY")

# Configure the Google Generative AI with the API key
genai.configure(api_key=api_key)

# Set the page configuration for the Streamlit app
st.set_page_config(
    page_title="Google Gemini Models",
    page_icon="🤖"
)

# Check if the Google API key is provided in the sidebar
with st.sidebar:
    if 'GOOGLE_API_KEY' in st.secrets:
        st.success('API key already provided!', icon='✅')
        api_key = st.secrets['GOOGLE_API_KEY']
    else:
        api_key = st.text_input('Enter Google API Key:', type='password')
        if not (api_key.startswith('AI')):
            st.warning('Please enter your API Key!', icon='⚠️')
        else:
            st.success('Success!', icon='✅')
    os.environ['GOOGLE_API_KEY'] = api_key
    "[Get a Google Gemini API key](https://ai.google.dev/)"
    "[View the source code](https://github.com/wms31/streamlit-gemini/blob/main/app.py)"
    "[Check out the blog post!](https://letsaiml.com/creating-google-gemini-app-with-streamlit/)"

# Set the title and caption for the Streamlit app
st.title("🤖 Google Gemini Models")
st.caption("🚀 A streamlit app powered by Google Gemini")

# Create tabs for the Streamlit app
tab1, tab2 = st.tabs(["🌏 Generate Travel Plans - Gemini Pro", "🖼️ Visual Venture - Gemini Pro Vision"])

# Code for Gemini Pro model
with tab1:
    st.write("💬 Using Gemini Pro - Text only model")
    st.subheader("🌏 Generate travel itineraries")
    
    destination_name = st.text_input("Enter destination name: \n\n",key="destination_name",value="United Arab Emirates")
    days = st.text_input("How many days would you like the itinerary to be? \n\n",key="days",value="5")
    suggested_attraction = st.text_input("What should the first suggested attraction be for the trip? \n\n",key="suggested_attraction",value="Visiting Burj Khalifa in Dubai.")
        
    prompt = f"""Come up with a {days}-day itinerary for a trip to {destination_name}. The first suggested attraction should be {suggested_attraction}
    """
    
    config = {
        "temperature": 0.8,
        "max_output_tokens": 2048,
        }
    
    generate_t2t = st.button("Generate my travel itinerary", key="generate_t2t")
    model = genai.GenerativeModel("gemini-pro", generation_config=config)
    if generate_t2t and prompt:
        with st.spinner("Generating your travel itinerary using Gemini..."):
            plan_tab, prompt_tab = st.tabs(["Travel Itinerary", "Prompt"])
            with plan_tab: 
                response = model.generate_content(prompt)
                if response:
                    st.write("Your plan:")
                    st.write(response.text)
            with prompt_tab: 
                st.text(prompt)

# Code for Gemini Pro Vision model
with tab2:
    st.write("🖼️ Using Gemini Pro Vision - Multimodal model")
    st.subheader("🔮 Generate image to text responses")
    
    image_prompt = st.text_input("Ask any question about the image", placeholder="Prompt", label_visibility="visible", key="image_prompt")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    image = ""

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image.", use_column_width=True)

    submit=st.button("Generate Response")

    if submit:
        model = genai.GenerativeModel('gemini-pro-vision')
        with st.spinner("Generating your response using Gemini..."):
            if image_prompt!="":
                response = model.generate_content([image_prompt,image])
            else:
                response = model.generate_content(image)
        response = response.text
        st.subheader("Gemini's response")
        st.write(response)

    
