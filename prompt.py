import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# URLs ของภาพ 3 รูป
image_urls = {
    "Bulldog Inglese": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Golden Retriever": "https://upload.wikimedia.org/wikipedia/commons/9/99/Golden_retriever_eating_pigs_foot.jpg",
    "Siberian Husky": "https://upload.wikimedia.org/wikipedia/commons/e/e9/Siberian_Husky_Belka.jpg"
}

st.title("เลือกภาพสุนัขเพื่อขยายเต็มจอ")

# sidebar สำหรับเลือกภาพ
selected_image_name = st.sidebar.radio("เลือกรูปภาพ", list(image_urls.keys()))

# โหลดภาพจาก URL ที่เลือก
response = requests.get(image_urls[selected_image_name])
img = Image.open(BytesIO(response.content))

# แสดงภาพขนาดเต็มจอ (กว้างเต็มพื้นที่)
st.image(img, caption=selected_image_name, use_column_width=True)
