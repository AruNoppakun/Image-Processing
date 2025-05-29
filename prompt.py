import streamlit as st
import requests
from PIL import Image
from io import BytesIO
import plotly.express as px
import pandas as pd

st.title("ปรับขนาดรูปย่อและดูแกน X-Y ของขนาดภาพ")

# URLs ของภาพทั้ง 3
image_urls = [
    "https://upload.wikimedia.org/wikipedia/commons/b/bf/Bulldog_inglese.jpg",
    "https://images.pexels.com/photos/50577/hedgehog-animal-baby-cute-50577.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=500",
    "https://images.dmc.tv/wallpaper/raw/7480.jpg"
]

# Slider ให้เลือกขนาดรูปย่อ (thumbnail)
thumb_size = st.slider("ปรับขนาดรูปย่อ (px)", min_value=50, max_value=400, value=200, step=10)

def load_and_resize(url, size=(200, 200)):
    response = requests.get(url)
    if response.status_code == 200:
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGB")
        img = img.resize(size)
        return img
    else:
        return None

images = [load_and_resize(url, (thumb_size, thumb_size)) for url in image_urls]

cols = st.columns(3)
selected_index = None

for i, col in enumerate(cols):
    if images[i] is not None:
        if col.button(f"เลือกภาพที่ {i+1}"):
            selected_index = i
        col.image(images[i], use_container_width=True)

# สร้าง DataFrame เก็บขนาดรูปภาพย่อ
data = {
    "Image": [f"ภาพที่ {i+1}" for i in range(len(images))],
    "Width": [img.width if img else 0 for img in images],
    "Height": [img.height if img else 0 for img in images],
}
df = pd.DataFrame(data)

# แสดงกราฟแกน X=Width, แกน Y=Height
fig = px.scatter(df, x="Width", y="Height", text="Image",
                 title="ขนาดรูปภาพย่อ (Width x Height)")

fig.update_traces(textposition='top center')
fig.update_layout(xaxis_title='ความกว้าง (px)', yaxis_title='ความสูง (px)', 
                  yaxis=dict(scaleanchor="x", scaleratio=1))  # ให้แกน X,Y สัดส่วนเท่ากัน

st.plotly_chart(fig, use_container_width=True)

# แสดงภาพขนาดเต็มเมื่อเลือก
if selected_index is not None:
    st.subheader(f"ภาพที่ {selected_index + 1} (ขนาดเต็ม)")
    response = requests.get(image_urls[selected_index])
    if response.status_code == 200:
        full_img = Image.open(BytesIO(response.content))
        st.image(full_img, use_container_width=True)
    else:
        st.error("ไม่สามารถโหลดภาพขนาดเต็มได้")
