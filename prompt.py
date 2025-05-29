import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt

st.title("ดูภาพพร้อมแกน X, Y และเลือกขนาดภาพ")

image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/3/32/French_Bulldog_with_Black_Mask.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/6e/EnglishBulldog.jpg"
]

thumb_size = st.slider("ปรับขนาดรูปย่อ (px)", 50, 400, 200, 10)

def load_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        return img
    return None

def plot_image_with_axes(img, size):
    fig, ax = plt.subplots(figsize=(size/100, size/100), dpi=100)
    ax.imshow(img.resize((size, size)))
    ax.set_xticks(range(0, size+1, 50))
    ax.set_yticks(range(0, size+1, 50))
    ax.grid(True, color='gray', linestyle='--', linewidth=0.5)
    ax.set_xlabel("X (pixels)")
    ax.set_ylabel("Y (pixels)")
    # กลับแกน y ให้เหมือนภาพปกติ (origin บนซ้าย)
    ax.invert_yaxis()
    plt.tight_layout()
    plt.axis('on')
    return fig

images = [load_image(url) for url in image_urls]

cols = st.columns(3)
selected_index = None

for i, col in enumerate(cols):
    if images[i] is not None:
        fig = plot_image_with_axes(images[i], thumb_size)
        if col.button(f"เลือกภาพที่ {i+1}"):
            selected_index = i
        col.pyplot(fig)

if selected_index is not None:
    st.subheader(f"ภาพที่ {selected_index + 1} (ขนาดเต็ม)")
    full_img = load_image(image_urls[selected_index])
    if full_img is not None:
        st.image(full_img, use_container_width=True)
    else:
        st.error("ไม่สามารถโหลดภาพขนาดเต็มได้")
