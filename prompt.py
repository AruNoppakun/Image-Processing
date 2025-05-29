import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np

st.title("แสดงภาพพร้อมแกน X, Y ด้วย matplotlib และปรับขนาดภาพเต็ม")

# URLs ของภาพทั้ง 3
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://images.dmc.tv/wallpaper/raw/7480.jpg",
    "https://waymagazine.org/wp-content/uploads/2019/05/dog.jpg"
]

# โหลดภาพเต็มไว้ก่อน
def load_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content)).convert("RGB")
        return img
    else:
        return None

full_images = [load_image(url) for url in image_urls]

# แสดงภาพย่อแบบ fixed size 150x150 px เพื่อเลือก
thumb_size = (150, 150)
thumb_images = [img.resize(thumb_size) if img else None for img in full_images]

cols = st.columns(3)
selected_index = None

for i, col in enumerate(cols):
    if thumb_images[i] is not None:
        if col.button(f"เลือกภาพที่ {i+1}"):
            selected_index = i
        col.image(thumb_images[i], use_container_width=True)

if selected_index is not None:
    st.subheader(f"ภาพที่ {selected_index + 1} (ขนาดเต็มพร้อมแกน X,Y)")

    # เลือกขนาดปรับภาพเต็ม (scale factor)
    scale = st.slider(
        "ปรับขนาดภาพเต็ม (scale factor)", min_value=0.1, max_value=2.0, value=1.0, step=0.1
    )

    img = full_images[selected_index]

    # ปรับขนาดภาพตาม scale factor โดยใช้ PIL resize
    new_size = (int(img.width * scale), int(img.height * scale))
    resized_img = img.resize(new_size)

    # แปลงเป็น numpy array สำหรับ plt
    img_np = np.array(resized_img)

    # แสดงภาพด้วย matplotlib พร้อมแกน X, Y
    fig, ax = plt.subplots(figsize=(new_size[0]/100, new_size[1]/100), dpi=100)
    ax.imshow(img_np)
    ax.set_xlabel("X (pixel)")
    ax.set_ylabel("Y (pixel)")
    ax.set_title("ภาพปรับขนาดพร้อมแกน X, Y")

    # กำหนดขอบเขตแกนให้ตรงกับขนาดภาพ
    ax.set_xlim(0, new_size[0])
    ax.set_ylim(new_size[1], 0)  # ปรับให้แกน Y เริ่มต้นที่บนสุดของภาพ

    # ตั้ง tick ให้เหมาะสม (5 ตำแหน่ง)
    ax.set_xticks(np.linspace(0, new_size[0], 5).astype(int))
    ax.set_yticks(np.linspace(0, new_size[1], 5).astype(int))

    st.pyplot(fig)
