import streamlit as st
import openai
import os

os.environ["OPENAI_API_KEY"] = "YOUR-API"
     
def main():
        
    page_bg_img = f"""
    <style>
    [data-testid="stAppViewContainer"] > .main {{
        background-image: url("https://images.unsplash.com/photo-1702816789113-bbc54df5f1aa?q=80&w=1932&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
        background-size: 110%;
        background-position: top left;
        background-repeat: no-repeat;
        background-attachment: fixed;
        }}

    [data-testid="stSidebar"] > div:first-child {{
    background-image: url("https://images.unsplash.com/photo-1702635429447-06e9ee0c617c?q=80&w=1974&auto=format&fit=crop&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8fA%3D%3D");
    background-size: 45%;
    background-position: top left;
    background-repeat: no-repeat;
    background-attachment: fixed;
    }}
        
    [data-testid="stHeader"] {{
        background: rgba(0,0,0,0);
        }}

    [data-testid="stToolbar"] {{
        right: 2rem;
        }}
    </style>
    """
    st.markdown(page_bg_img, unsafe_allow_html=True)

    st.sidebar.title('OpenAI Text 💬 to image generator 📸')
    st.sidebar.info('🐥 Generate an image using Generative AI by describing what you want to see, all images are published publicly by default. 🐤')
    st.title(" 🐱‍🏍 AI Image Generator")
    st.info(""" You can download image by right clicking\
            on the image and select save image as option""")
   
    with st.form(key='form'):
        prompt = st.text_input(label='What do you want to see❓ 🤖')
        size = st.selectbox('Select size of the images ', ('256x256', '512x512', '1024x1024'))
        num_images = st.selectbox('Enter number of images to be generated ✅', (1,2,3,4))
        submit_button = st.form_submit_button(label='Submit')

    if submit_button:
        if prompt:
            response = openai.Image.create(
                prompt = prompt,
                n = num_images,
                size=size,
            )

            for idx in range(num_images):
                image_url = response["data"][idx]["url"]

                st.image(image_url, caption=f"Generate image: {idx+1}",
                         use_column_width=True)
                

if __name__ == "__main__":
    main()