import streamlit as st
from PIL import Image
import requests
import torch
import io

# โหลด YOLOv5 model
@st.cache_resource
def load_model():
    model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)
    return model

model = load_model()

st.title("🔍 ตรวจจับวัตถุในภาพ (Object Detection)")
st.write("อัปโหลดภาพหรือใส่ URL ของภาพเพื่อดูวัตถุที่ตรวจพบ")

# ตัวเลือกการป้อนภาพ
option = st.radio("เลือกรูปแบบการนำเข้าภาพ:", ('URL', 'อัปโหลดไฟล์'))

image = None

if option == 'URL':
    url = st.text_input("ใส่ URL ของภาพ:")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content))
        except:
            st.error("ไม่สามารถโหลดภาพจาก URL ได้ กรุณาตรวจสอบลิงก์")
elif option == 'อัปโหลดไฟล์':
    uploaded_file = st.file_uploader("อัปโหลดไฟล์ภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)

# ตรวจจับวัตถุในภาพ
if image:
    st.image(image, caption='ภาพที่เลือก', use_column_width=True)
    st.write("กำลังประมวลผล...")

    results = model(image)

    # แสดงภาพที่มีการตรวจจับวัตถุ
    results.render()  # แก้ไขใน place

    st.image(results.ims[0], caption="ผลลัพธ์การตรวจจับ", use_column_width=True)

    # แสดงรายการวัตถุที่พบ
    labels = results.pandas().xyxy[0]['name'].value_counts()
    st.subheader("วัตถุที่พบในภาพ:")
    for label, count in labels.items():
        st.write(f"- {label} ({count} ชิ้น)")
