import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# URLs ของภาพ 3 รูป
image_urls = {
    "Bulldog Inglese": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Golden Retriever": "https://upload.wikimedia.org/wikipedia/commons/8/86/Golden_Retriever_Carlos_(10581910556).jpg",
    "Siberian Husky": "https://upload.wikimedia.org/wikipedia/commons/6/65/Siberian_Husky_female.jpg"
}

# โหลดภาพจาก URL
def load_image(url):
    response = requests.get(url)
    return Image.open(BytesIO(response.content))

# สร้างลิสต์ชื่อภาพสำหรับ selectbox
image_names = list(image_urls.keys())

# เลือกรูปภาพ
selected_name = st.selectbox("เลือกภาพเพื่อขยายเต็มจอ", image_names)

# โหลดและแสดงภาพที่เลือก
img = load_image(image_urls[selected_name])
st.image(img, caption=selected_name, use_column_width=True)
