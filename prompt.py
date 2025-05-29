import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

# รายชื่อภาพพร้อม URL
image_dict = {
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://images.pexels.com/photos/50577/hedgehog-animal-baby-cute-50577.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
    "https://cdn.pixabay.com/photo/2023/11/09/19/36/zoo-8378189_1280.jpg"
}

st.title("แสดงภาพสัตว์สามชนิด")

cols = st.columns(3)
target_size = (300, 300)

# กำหนดค่าเริ่มต้น session_state สำหรับเก็บภาพที่เลือก
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# แสดงภาพย่อพร้อมปุ่มเลือก
for i, (caption, url) in enumerate(image_dict.items()):
    with cols[i]:
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize(target_size)
        st.image(img, caption=caption, use_container_width=True)

        if st.button("เลือกรูปภาพ", key=f"select_{i}"):
            st.session_state.selected_image = (caption, url)

# แสดงภาพขนาดเต็มถ้ามีการเลือกภาพ
if st.session_state.selected_image is not None:
    caption, url = st.session_state.selected_image
    response = requests.get(url)
    img_full = Image.open(BytesIO(response.content))

    # เพิ่ม slider ให้ปรับความกว้างภาพเต็ม (px)
    width = st.slider("ปรับความกว้างภาพเต็ม (pixel)", min_value=100, max_value=1200, value=600)

    # ปรับขนาดภาพให้กว้างตาม slider รักษาอัตราส่วน
    aspect_ratio = img_full.height / img_full.width
    new_height = int(width * aspect_ratio)
    img_full_resized = img_full.resize((width, new_height))

    st.markdown("---")
    st.write(f"ขนาดภาพ (Width x Height): {img_full_resized.width} px x {img_full_resized.height} px")

    # แสดงภาพด้วย matplotlib พร้อมแกน X, Y
    fig, ax_orig = plt.subplots()
    ax_orig.imshow(img_full_resized)
    ax_orig.set_xlabel("X (Column)")
    ax_orig.set_ylabel("Y (Row)")
    ax_orig.set_title(f"ภาพเต็ม: {caption}")

    st.pyplot(fig)
