import streamlit as st
from PIL import Image
import requests
import io
from ultralytics import YOLO
from collections import Counter

st.title("🧠 ตรวจจับวัตถุในภาพด้วย YOLOv8")

# โหลดโมเดล YOLOv8 nano (เล็กและเร็ว)
@st.cache_resource
def load_model():
    return YOLO("yolov8n.pt")  # ใช้ yolov8n.pt ที่เบาและโหลดเร็ว

model = load_model()

# ตัวเลือกการป้อนภาพ
option = st.radio("เลือกรูปแบบการป้อนภาพ", ['URL', 'อัปโหลดไฟล์'])

image = None
if option == 'URL':
    url = st.text_input("ใส่ URL ของภาพ")
    if url:
        try:
            response = requests.get(url)
            image = Image.open(io.BytesIO(response.content)).convert("RGB")
        except:
            st.error("ไม่สามารถโหลดภาพจาก URL นี้ได้")
elif option == 'อัปโหลดไฟล์':
    uploaded_file = st.file_uploader("เลือกรูปภาพ", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")

# ตรวจจับและแสดงผล
if image:
    st.image(image, caption="ภาพต้นฉบับ",use_column_width =True)
    st.write("🔍 กำลังตรวจจับวัตถุ...")

    results = model(image)

    # วาดภาพที่มี bounding boxes
    annotated_image = results[0].plot()
    st.image(annotated_image, caption="ผลการตรวจจับ",use_column_width =True)

    # แสดงรายการวัตถุ
    st.subheader("วัตถุที่ตรวจพบ:")
    names = results[0].names
    classes = results[0].boxes.cls.cpu().numpy()
    counts = Counter([names[int(c)] for c in classes])
    for name, count in counts.items():
        st.write(f"- {name}: {count} ชิ้น")
