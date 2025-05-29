import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# URLs ของภาพทั้ง 3
image_urls = {
    "Bulldog (หมา)": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Cat (แมว)": "https://upload.wikimedia.org/wikipedia/commons/3/3a/Cat03.jpg",
    "Monkey (ลิง)": "https://upload.wikimedia.org/wikipedia/commons/e/e3/Capuchin_Costa_Rica_03.jpg"
}

st.title("แสดงภาพสัตว์สามชนิด")

for caption, url in image_urls.items():
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.image(img, caption=caption)
