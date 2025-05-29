import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# รายการ URL ภาพ
image_urls = {
    "Bulldog Inglese": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Golden Retriever": "https://upload.wikimedia.org/wikipedia/commons/5/5e/Golden_Retriever_medium-to-light_coat.jpg",
    "Siberian Husky": "https://upload.wikimedia.org/wikipedia/commons/1/12/Siberian_Husky_pho.jpg"
}

# สร้าง selectbox ให้เลือกภาพ
selected_image_name = st.selectbox("เลือกภาพที่ต้องการดู", list(image_urls.keys()))

# โหลดภาพที่เลือก
url = image_urls[selected_image_name]
response = requests.get(url)
img = Image.open(BytesIO(response.content))

# แสดงภาพแบบเต็มพื้นที่กว้าง
st.image(img, caption=selected_image_name, use_column_width=True)
