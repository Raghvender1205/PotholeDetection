from ultralytics import YOLO
import streamlit as st
import subprocess
import os
import cv2


# file = r'D:\ML_RESEARCH\PotholeDetection\Deployment\test_videos\street2.mp4'
# model = YOLO('best.pt')
# results = model(file)
# print(results)
# os.system(f'yolo task=detect mode=predict model=best.pt source={file} hide_labels=True save show')
# st.video(r'Deployment\runs\detect\predict\street2.mp4')

st.title('Upload Video')
file = st.file_uploader('Upload Video', type=['mp4'])

if st.button('Detect') and file is not None:
    st.video(file)
    cmd = f'yolo task=detect mode=predict model=best.pt source=test_videos/{file.name} hide_labels=True show=True'
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, err = process.communicate()

    if output:
        st.text(output.decode('utf-8'))
    if err:
        st.error(err.decode('utf-8'))