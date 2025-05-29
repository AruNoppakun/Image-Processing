import streamlit as st
from PIL import Image
import requests
from io import BytesIO
import matplotlib.pyplot as plt

# รายชื่อภาพพร้อม URL
image_dict = {
    "Bulldog (หมา)": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Cat (แมว)": "https://images.pexels.com/photos/50577/hedgehog-animal-baby-cute-50577.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
    "Monkey (ลิง)": "https://cdn.pixabay.com/photo/2023/11/09/19/36/zoo-8378189_1280.jpg"
}

def load_image(url):
    response = requests.get(url)
    img = Image.open(BytesIO(response.content)).convert("RGBA")
    return img

st.title("แสดงภาพสัตว์สามชนิด")

cols = st.columns(3)
target_size = (300, 300)

# กำหนดค่าเริ่มต้น session_state สำหรับเก็บภาพที่เลือก
if "selected_image" not in st.session_state:
    st.session_state.selected_image = None

# แสดงภาพย่อพร้อมปุ่มเลือก
for i, (caption, url) in enumerate(image_dict.items()):
    with cols[i]:
        img = load_image(url)
        img_resized = img.resize(target_size)
        st.image(img_resized, caption=caption, use_container_width=True)

        if st.button("เลือกรูปภาพ", key=f"select_{i}"):
            st.session_state.selected_image = (caption, url)

# แสดงภาพขนาดเต็มถ้ามีการเลือกภาพ
if st.session_state.selected_image is not None:
    caption, url = st.session_state.selected_image
    img_full = load_image(url)

    # slider ปรับความกว้างภาพเต็ม
    width = st.slider("ปรับความกว้างภาพเต็ม (pixel)", min_value=100, max_value=1200, value=600)
    aspect_ratio = img_full.height / img_full.width
    new_height = int(width * aspect_ratio)
    img_full_resized = img_full.resize((width, new_height))

    st.markdown("---")
    st.write(f"ขนาดภาพ (Width x Height): {img_full_resized.width} px x {img_full_resized.height} px")

    # แสดงภาพเต็มพร้อมแกน
    fig, ax_orig = plt.subplots()
    ax_orig.imshow(img_full_resized)
    ax_orig.set_xlabel("X (Column)")
    ax_orig.set_ylabel("Y (Row)")
    ax_orig.set_title(f"ภาพเต็ม: {caption}")
    st.pyplot(fig)

st.markdown("---")
st.header("Blended Image (ผสมภาพ)")

# เลือกภาพสองภาพสำหรับผสม
img_names = list(image_dict.keys())
img1_name = st.selectbox("เลือกภาพที่ 1", img_names, index=0)
img2_name = st.selectbox("เลือกภาพที่ 2", img_names, index=1 if len(img_names)>1 else 0)

if img1_name == img2_name:
    st.warning("กรุณาเลือกภาพคนละภาพสำหรับผสม")
else:
    img1 = load_image(image_dict[img1_name])
    img2 = load_image(image_dict[img2_name])

    # ปรับขนาดให้เท่ากัน (ขนาดของภาพที่ 1)
    img2_resized = img2.resize(img1.size)

    # slider ปรับค่า alpha
    alpha = st.slider("ปรับค่า Alpha (ความโปร่งแสงของภาพที่ 2)", 0.0, 1.0, 0.5)

    # ผสมภาพ
    blended = Image.blend(img1, img2_resized, alpha)

    st.image(blended, caption=f"Blended Image: {img1_name} + {img2_name} (Alpha={alpha:.2f})", use_container_width=True)
