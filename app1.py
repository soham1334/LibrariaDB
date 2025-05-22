

import streamlit as st
import base64

image_file = r"C:\Users\SOHAM\Desktop\Libradb\library_img.jpg"

def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set your local image path here
set_background(image_file)


st.markdown("""
    <div style="
        background-color: rgba(0, 0, 0, 0.6);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
    ">
        <h1 style="color: white; font-size: 50px; margin: 0;">
            Libraria <span style="color: yellow;">AI</span>
        </h1>
        <p style="
            color: white;
            font-size: 20px;
            font-style: italic;
            font-family: 'Georgia', serif;
            margin-top: 10px;
        ">
            "Automate. Organize. Discover — with your smart library companion."
        </p>
    </div>
""", unsafe_allow_html=True)



st.markdown("<h3>Question:</h3>", unsafe_allow_html=True)
Question = st.text_input("", placeholder="Write here.....")

@st.cache_data
def load_data():
    from backend import Queries

    return Queries

Queries = load_data()
if Question:
    response = Queries(Question)
    formatted_response = response.replace('\n', '<br>') 

    st.markdown("<h3>Response:</h3>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            color: white;
            font-size: 18px;
            font-family: 'Segoe UI', sans-serif;
            border: 1px solid rgba(255, 255, 255, 0.3);
            max-width: 80%;
            margin-top: 10px;
        ">
            {formatted_response}
        </div>
    """, unsafe_allow_html=True)


    
  

=======

import streamlit as st
import base64

image_file = r"C:\Users\SOHAM\Desktop\Libradb\library_img.jpg"

def set_background(image_file):
    with open(image_file, "rb") as file:
        encoded = base64.b64encode(file.read()).decode()

    css = f"""
    <style>
    [data-testid="stAppViewContainer"] {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
        background-position: center;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# Set your local image path here
set_background(image_file)


st.markdown("""
    <div style="
        background-color: rgba(0, 0, 0, 0.6);
        padding: 30px;
        border-radius: 20px;
        text-align: center;
        margin-bottom: 30px;
    ">
        <h1 style="color: white; font-size: 50px; margin: 0;">
            Libraria <span style="color: yellow;">AI</span>
        </h1>
        <p style="
            color: white;
            font-size: 20px;
            font-style: italic;
            font-family: 'Georgia', serif;
            margin-top: 10px;
        ">
            "Automate. Organize. Discover — with your smart library companion."
        </p>
    </div>
""", unsafe_allow_html=True)



st.markdown("<h3>Question:</h3>", unsafe_allow_html=True)
Question = st.text_input("", placeholder="Write here.....")

@st.cache_data
def load_data():
    from backend import Queries

    return Queries

Queries = load_data()
if Question:
    response = Queries(Question)
    formatted_response = response.replace('\n', '<br>') 

    st.markdown("<h3>Response:</h3>", unsafe_allow_html=True)

    st.markdown(f"""
        <div style="
            background: rgba(255, 255, 255, 0.15);
            padding: 20px;
            border-radius: 15px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            color: white;
            font-size: 18px;
            font-family: 'Segoe UI', sans-serif;
            border: 1px solid rgba(255, 255, 255, 0.3);
            max-width: 80%;
            margin-top: 10px;
        ">
            {formatted_response}
        </div>
    """, unsafe_allow_html=True)


    
  

