import streamlit as st
from PIL import Image
import requests
from io import BytesIO

# รายชื่อภาพพร้อม URL
image_dict = {
    "Bulldog (หมา)": "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "Cat (แมว)": "https://f.ptcdn.info/002/048/000/oidav7m4nF0JGvXz44Y-o.jpg",
    "Monkey (ลิง)": "https://cdn.pixabay.com/photo/2023/11/09/19/36/zoo-8378189_1280.jpg"
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
        # โหลดภาพและปรับขนาด
        response = requests.get(url)
        img = Image.open(BytesIO(response.content))
        img = img.resize(target_size)

        # แสดงภาพและ caption
        st.image(img, caption=caption, use_container_width=True)

        # ปุ่มเลือกภาพ
        if st.button("เลือกรูปภาพ", key=f"select_{i}"):
            st.session_state.selected_image = (caption, url)

# แสดงภาพขนาดเต็มถ้ามีการเลือกภาพ
if st.session_state.selected_image is not None:
    caption, url = st.session_state.selected_image
    response = requests.get(url)
    img_full = Image.open(BytesIO(response.content))

    st.markdown("---")
    st.image(img_full, caption=f"ภาพเต็ม: {caption}", use_container_width=True)
