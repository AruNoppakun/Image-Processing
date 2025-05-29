import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("คลิกเลือกรูปภาพเพื่อดูขนาดเต็ม และปรับขนาดรูปย่อได้")

# URLs ของภาพทั้ง 3
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/32/French_Bulldog_with_Black_Mask.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/6e/EnglishBulldog.jpg"
]

# Slider ให้เลือกขนาดรูปย่อ (thumbnail)
thumb_size = st.slider("ปรับขนาดรูปย่อ (px)", min_value=50, max_value=400, value=200, step=10)

# โหลดและย่อภาพตามขนาดที่เลือก
def load_and_resize(url, size=(200, 200)):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img = img.resize(size)
        return img
    else:
        return None

# โหลดภาพย่อตามขนาด slider
images = [load_and_resize(url, (thumb_size, thumb_size)) for url in image_urls]

cols = st.columns(3)
selected_index = None

for i, col in enumerate(cols):
    if images[i] is not None:
        if col.button(f"เลือกภาพที่ {i+1}"):
            selected_index = i
        col.image(images[i], use_container_width=True)

if selected_index is not None:
    st.subheader(f"ภาพที่ {selected_index + 1} (ขนาดเต็ม)")
    response = requests.get(image_urls[selected_index])
    if response.status_code == 200:
        full_img = Image.open(BytesIO(response.content))
        st.image(full_img, use_container_width=True)
    else:
        st.error("ไม่สามารถโหลดภาพขนาดเต็มได้")
