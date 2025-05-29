import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# URLs ของภาพทั้ง 3
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/32/French_Bulldog_with_Black_Mask.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/6e/EnglishBulldog.jpg"
]

st.title("คลิกเลือกรูปภาพเพื่อดูขนาดเต็ม")

# โหลดภาพทั้งหมดจาก URL
images = []
for url in image_urls:
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        images.append(img)
    else:
        images.append(None)

# แสดงภาพเป็นแถวแนวนอน
cols = st.columns(3)
selected_index = None

for i, col in enumerate(cols):
    if images[i] is not None:
        if col.button(f"เลือกภาพที่ {i+1}"):
            selected_index = i
        col.image(images[i], use_column_width=True)

# แสดงภาพขนาดเต็มเมื่อเลือก
if selected_index is not None:
    st.subheader(f"ภาพที่ {selected_index + 1} (ขนาดเต็ม)")
    st.image(images[selected_index], use_column_width=True)
