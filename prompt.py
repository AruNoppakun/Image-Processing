import streamlit as st
import requests
from PIL import Image
from io import BytesIO

# รายการ URL รูปภาพ
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/6/6e/Golde33443.jpg",
    "https://upload.wikimedia.org/wikipedia/commons/e/e5/Labrador_Retriever_portrait.jpg"
]

# หัวข้อ
st.title("แกลเลอรีรูปภาพสุนัข")

# แสดงภาพแบบ thumbnail
st.subheader("เลือกรูปภาพที่ต้องการดูแบบขยาย")
cols = st.columns(len(image_urls))
images = []

for i, url in enumerate(image_urls):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        images.append(img)
        with cols[i]:
            st.image(img, caption=f"รูปที่ {i+1}", use_column_width=True)
    else:
        images.append(None)
        with cols[i]:
            st.error("โหลดรูปไม่สำเร็จ")

# ตัวเลือกสำหรับเลือกภาพ
selected_index = st.selectbox("เลือกรูปภาพเพื่อดูแบบขยาย", options=range(len(images)), format_func=lambda i: f"รูปที่ {i+1}")

# แสดงภาพเต็ม
if images[selected_index]:
    st.subheader(f"รูปที่ {selected_index + 1} แบบขยาย")
    st.image(images[selected_index], use_column_width=True)
else:
    st.error("ไม่สามารถแสดงภาพที่เลือกได้")
