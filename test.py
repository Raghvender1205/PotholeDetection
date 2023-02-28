from ultralytics import YOLO
import streamlit as st
import os

file = r'D:\ML_RESEARCH\PotholeDetection\Deployment\test_videos\street2.mp4'
# model = YOLO('best.pt')
# results = model(file)
# print(results)
os.system(f'yolo task=detect mode=predict model=best.pt source={file} hide_labels=True save')
st.video(r'Deployment\runs\detect\predict\street2.mp4')