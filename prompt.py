import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# URLs ของภาพแบบ list
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://f.ptcdn.info/002/048/000/oidav7m4nF0JGvXz44Y-o.jpg",
    "https://cdn.pixabay.com/photo/2023/11/09/19/36/zoo-8378189_1280.jpg"
]

st.title("แสดงภาพสัตว์สามชนิด")

cols = st.columns(3)

for col, url in zip(cols, image_urls):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    col.image(img, use_container_width=True)
