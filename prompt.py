import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# รายชื่อภาพพร้อม URL
image_dict = {
    "Bulldog (หมา)": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Cat (แมว)": "https://f.ptcdn.info/002/048/000/oidav7m4nF0JGvXz44Y-o.jpg",
    "Monkey (ลิง)": "https://cdn.pixabay.com/photo/2023/11/09/19/36/zoo-8378189_1280.jpg"
}

st.title("แสดงภาพสัตว์สามชนิด")

cols = st.columns(3)
target_size = (300, 300)

# แสดงภาพย่อในคอลัมน์
for col, (caption, url) in zip(cols, image_dict.items()):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img = img.resize(target_size)
    col.image(img, caption=caption, use_container_width=True)

# ตัวเลือกให้ผู้ใช้เลือกภาพเพื่อดูเต็มจอ
selected_caption = st.selectbox("เลือกภาพเพื่อขยายเต็มจอ", list(image_dict.keys()))

# โหลดและแสดงภาพขนาดเต็มตามที่เลือก
selected_url = image_dict[selected_caption]
response = requests.get(selected_url)
img_full = Image.open(BytesIO(response.content))

st.image(img_full, caption=f"ภาพเต็ม: {selected_caption}", use_container_width=True)
