import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# ตั้งชื่อหัวข้อ
st.title("แสดงภาพจาก URL")

# URL ของภาพ
image_url = "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg"

# ดาวน์โหลดภาพ
response = requests.get(image_url)
if response.status_code == 200:
    image = Image.open(BytesIO(response.content))
    st.image(image, caption="Bulldog Inglese", use_column_width=True)
else:
    st.error("ไม่สามารถโหลดภาพได้จาก URL ที่กำหนด")
