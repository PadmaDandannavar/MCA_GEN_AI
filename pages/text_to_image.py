import streamlit as st
import openai
import requests
from PIL import Image #Pillow
import io
import os 
from datetime import datetime
from dotenv import load_dotenv #to import serial key

#Load envt
load_dotenv() # load the serial key from dotenv

#configure the page
st.set_page_config(page_title="AI Image Generator Hub", #set complete canvas of the application
                   page_icon="+^",
                   layout="wide") 

#Title and Description

st.title("AI Image Generator")
st.markdown("Generate Stunning images from text description using OpenAI's DALLE - E Model")

#divide canvas 

st.sidebar.header("Settings")

# API KEY INPUT - CHECK ENVT VARIABLE FIRST
#default_api_key - variable to hold the API KEY  
default_api_key = os.getenv("OPENAI_API_KEY", "") 
if default_api_key:
    st.sidebar.success("API KEY loaded from the environment")
    api_key = default_api_key
else: #if api key is not in the envt get it from user
    api_key = st.sidebar.text_input("OpenAI API Key",type="password", help="Enter Your OpenAI API key")
    #st.sidebar.info("Get your API key from https://platform.openai.com/api-keys and paste it here.")

if api_key:
    openai.api_key = api_key

    #Image Generator Parameter
    st.sidebar.subheader("Generate Paramater")
    #Model Slection
    model = st.sidebar.selectbox(
        "Model", 
        ["dall-e-3", "dall-e-2"],
        help="Choose the DALL-E Model Version"
    )

    #Image Size
    if model == "dall-e-3":
        size_option  = ["1024x1024", "1024x1792", "1792x1024"]
    else:
        size_option = ["256x256", "512x512","1024x1024"]

    size = st.sidebar.selectbox("Image Size", size_option)  # fixed _selectbox typo

    #Image Quality (only for dall-e-3)
    if model == "dall-e-3":
        quality = st.sidebar.selectbox("Quality", ["standard", "hd"])  # lowercase for API
    else:
        quality = "standard"

    #style   (only for dall-e-3)
    if model == "dall-e-3":
        style = st.sidebar.selectbox("Style",["vivid","natural"])
    else:
        style = "natural"  # fixed typo

    if model == "dall-e-2":
        n_images= st.sidebar.slider("Number of Images",1,4,1) # fixed typo
    else:
        n_images = 1

#Main Content Area

col1,col2 = st.columns([1,1])

with col1:
    st.subheader("Text Prompt")

    #sample Prompts
    st.markdown("** Quick Start - Sample Prompts:**")

    sample_prompts = {
        "Landscapes": [
            "A serene mountain landscape at sunset with a crystal-clear lake",
            "A tropical beach with palm trees and turquoise water",
            "A misty forest with tall pine trees and morning sunlight"
        ],
        "Fantasy": [
            "A majestic dragon flying over a medieval castle",
            "A magical forest with glowing mushrooms and fairy lights",
            "A steampunk airship floating in cloudy skies"
        ],
        "Modern": [
            "A futuristic cityscape with flying cars and neon lights",
            "A cozy coffee shop with warm lighting and people reading",
            "A modern minimalist living room with large windows"
        ]
    } 

    selected_category = st.selectbox("Category", list(sample_prompts.keys()))
    selected_prompts = st.selectbox("Sample Prompt", sample_prompts[selected_category])

    if st.button("Use This Prompt"):
        #create the session state
        st.session_state.prompt_text = selected_prompts 

    #Text Input - custom prompt by user
    prompt = st.text_area(
        "Custom Prompt:",
        value=st.session_state.get('prompt_text',''),  # fixed capitalization
        placeholder= "A scenic landscape with mountain, a lake, and a sunset sky...",
        height = 150
    )

    #Generate button
    if st.button("GENERATE IMAGE", type="primary", disabled=not (api_key and prompt)):
        if not api_key:
            st.error("Please enter your OpenAI Key in the Sidebar")
        elif not prompt:
            st.error("Please enter a text prompt")
        else:
            try:
                with st.spinner("Generating Image... This may take a few seconds"):
                    # Use new OpenAI API for image generation
                    response = openai.images.generate(
                        prompt=prompt,
                        model=model,
                        size=size,
                        quality=quality if model=="dall-e-3" else None,
                        style=style if model=="dall-e-3" else None,
                        n=n_images
                    )
                    # store generated images in session state
                    st.session_state.generated_images = response.data
                    st.session_state.current_prompt = prompt
                    st.success("Image Generated Successfully")
            except Exception as e:
                if "401" in str(e) or "Incorrect API key" in str(e):
                    st.error("Authentication failed: Incorrect API key. Please check your OpenAI API key and try again.")
                else:
                    st.error(f"Error Generating Image: {str(e)}")

with col2:
     st.subheader("Generated Images")

     #display generated images

     if hasattr(st.session_state,'generated_images') and st.session_state.generated_images:
          for i, image_data in enumerate(st.session_state.generated_images):
                 try:
                    #download and display image
                    image_response = requests.get(image_data.url)
                    image = Image.open(io.BytesIO(image_response.content))

                    st.image(image, caption=f"Generated Image {i+1}", use_column_width = True)

                    #download button
                    img_buffer = io.BytesIO()
                    image.save(img_buffer, format='PNG')
                    img_buffer.seek(0)

                    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")  # fixed hour format

                    filename = f"generated_image_{timestamp}_{i+1}.png"

                    st.download_button(
                         label=f"Download Image",
                         data=img_buffer.getvalue(),  # fixed typo: 'date' -> 'data'
                         file_name=filename,
                         mime="image/png"
                    )

                    #show prompt used
                    if hasattr(st.session_state, 'current_prompt'):
                         st.caption(f"Prompt: {st.session_state.current_prompt}")  # fixed typo
                 except Exception as e:
                    st.error(f"Error Display Image {i+1}: {str(e)}")
     else:
          st.info("Generated Images will appear here")










