import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# URLs ของภาพทั้ง 3
image_urls = {
    "Bulldog (หมา)": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Cat (แมว)": "https://f.ptcdn.info/002/048/000/oidav7m4nF0JGvXz44Y-o.jpg",
    "Monkey (ลิง)": "https://themomentum.co/wp-content/uploads/2020/02/%E0%B8%AA%E0%B8%B1%E0%B8%95%E0%B8%A7%E0%B9%8C%E0%B8%9B%E0%B9%88%E0%B8%B2-Thumbnail.png"
}

st.title("แสดงภาพสัตว์สามชนิด")

for caption, url in image_urls.items():
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    st.image(img, caption=caption)
