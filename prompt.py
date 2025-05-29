import streamlit as st
import requests
from PIL import Image
from io import BytesIO

st.title("เลือกภาพเพื่อขยาย")

# URLs ของภาพทั้ง 3
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://encrypted-tbn1.gstatic.com/images?q=tbn:ANd9GcQUEQYeiKkhn687htVNpGATyROPyOpuBIyrRpJrWMXaa1p-w5dFOT-z_znAjv0Tw8LC9nopCkxT-mGLoJZJt1RISSSlXVE5_mzjQAt2QzIC5Q",
    "https://s.isanook.com/ca/0/ud/276/1380909/12794445_1218908274799864_3867112738991391881_n.jpg"
]

# ฟังก์ชันดาวน์โหลดและเปิดภาพ
def load_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return Image.open(BytesIO(response.content))
    else:
        return None

# โหลดภาพทั้งหมดไว้ใน list
images = [load_image(url) for url in image_urls]

# กำหนดขนาดภาพที่จะแสดงในหน้าแรก (thumbnail size)
thumbnail_size = (250, 250)

# สร้าง session state สำหรับเก็บภาพที่ถูกเลือก
if "selected_index" not in st.session_state:
    st.session_state.selected_index = None

# แสดงภาพแบบย่อใน 3 คอลัมน์
cols = st.columns(3)
for idx, col in enumerate(cols):
    if images[idx]:
        # สร้างสำเนาภาพย่อ (thumbnail) ขนาดเท่ากัน
        thumb = images[idx].copy()
        thumb.thumbnail(thumbnail_size)
        # แสดงภาพพร้อมปุ่มคลิกเลือก
        if col.button(f"เลือกรูปที่ {idx + 1}"):
            st.session_state.selected_index = idx
        col.image(thumb, use_container_width=True) 

# ถ้ามีการเลือกภาพ ให้แสดงภาพขนาดเต็มด้านล่าง
if st.session_state.selected_index is not None:
    st.markdown("---")
    st.subheader(f"ภาพขนาดเต็ม - รูปที่ {st.session_state.selected_index + 1}")
    st.image(images[st.session_state.selected_index], use_container_width=True)
