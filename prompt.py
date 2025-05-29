import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("คลิกเลือกรูปภาพเพื่อดูขนาดเต็ม และปรับขนาดรูปย่อได้")

# URLs ของภาพทั้ง 3
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://images.dmc.tv/wallpaper/raw/3245.jpg",
    "https://images.pexels.com/photos/50577/hedgehog-animal-baby-cute-50577.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500"
]

# Slider ให้เลือกขนาดรูปย่อ (px)
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

# แสดงภาพใน 3 คอลัมน์
cols = st.columns(3)
selected_index = None

for i, col in enumerate(cols):
    if images[i] is not None:
        if col.button(f"เลือกภาพที่ {i+1}"):
            selected_index = i
        col.image(images[i], use_container_width=True)

# แสดงกราฟแกน X (width) และแกน Y (height) ของภาพย่อ
widths = [img.width if img else 0 for img in images]
heights = [img.height if img else 0 for img in images]
labels = [f"ภาพ {i+1}" for i in range(len(images))]

fig, ax = plt.subplots()
ax.bar(labels, widths, label='ความกว้าง (X)', alpha=0.7)
ax.bar(labels, heights, label='ความสูง (Y)', alpha=0.7, bottom=widths)

ax.set_ylabel("ขนาด (pixels)")
ax.set_title("ขนาดแกน X และ Y ของภาพย่อ")
ax.legend()

st.pyplot(fig)

# แสดงภาพขนาดเต็มเมื่อเลือก
if selected_index is not None:
    st.subheader(f"ภาพที่ {selected_index + 1} (ขนาดเต็ม)")
    response = requests.get(image_urls[selected_index])
    if response.status_code == 200:
        full_img = Image.open(BytesIO(response.content))
        st.image(full_img, use_container_width=True)
    else:
        st.error("ไม่สามารถโหลดภาพขนาดเต็มได้")
