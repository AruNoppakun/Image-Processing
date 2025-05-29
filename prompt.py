import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# URL ของภาพ
image_url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg"

# โหลดภาพจาก URL
response = requests.get(image_url)
img = Image.open(BytesIO(response.content))

# แสดงภาพบน Streamlit
st.image(img, caption="Bulldog Inglese")
