import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# URLs ของภาพทั้ง 3
image_urls = {
    "Bulldog (หมา)": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Cat (แมว)": "https://f.ptcdn.info/002/048/000/oidav7m4nF0JGvXz44Y-o.jpg",
    "Monkey (ลิง)": "https://www.khaoyainationalpark.com/application/files/6116/3273/3973/33.jpg"
}

st.title("แสดงภาพสัตว์สามชนิด")

# สร้าง 3 คอลัมน์เท่า ๆ กัน
cols = st.columns(3)

for col, (caption, url) in zip(cols, image_urls.items()):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    # ใส่ภาพลงในคอลัมน์ พร้อม caption
    col.image(img, caption=caption, use_column_width=True)
