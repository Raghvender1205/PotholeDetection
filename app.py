import streamlit as st
import cv2
import os

def run_model(file):
    cmd = f'yolo task=detect mode=predict model=best.pt source=test_videos/{file} imgsz=1280 hide_labels=True save=True'
    os.system(cmd)


st.title('Pothole Detection')
uploaded_file = st.file_uploader('Choose a video file', type=['mp4', 'mov', 'avi'])

# def write_bytesio(file, bytesio):
#     with open(file, 'wb') as f:
#         f.write(bytesio.getbuffer())

# tmp_file_to_save = './tmp/tmp_file.mp4'
# tmp_file_result = './tmp/tmp_res.mp4'
# if uploaded_file:
#     write_bytesio(tmp_file_to_save, uploaded_file)
#     cap = cv2.VideoCapture(tmp_file_to_save)

if st.button('Detect') and uploaded_file is not None:
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    run_model(uploaded_file.name)
    os.remove(uploaded_file.name)
    out = f'runs/detect/predict/{uploaded_file.name}'
    res = open(out, 'rb')
    video_bytes = res.read()
    st.video(video_bytes)
    os.remove(out)
    
    
