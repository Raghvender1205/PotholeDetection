import streamlit as st
import torch
from ultralytics import YOLO
import cv2
import numpy as np
import tempfile
import os
from werkzeug.utils import secure_filename

# https://docs.ultralytics.com/predict/
# https://github.com/ultralytics/ultralytics/blob/main/ultralytics/yolo/data/build.py#L135
# https://docs.ultralytics.com/engine/



@st.cache(allow_output_mutation=True)
def load_model():
    model_pth = 'best.pt'

    return YOLO(model_pth)

def app():
    st.set_page_config(page_title='Pothole Detection', page_icon=':smile:', layout='wide')
    model = load_model()

    file = st.file_uploader('Upload a Video File', type=['mp4', 'mov', 'avi'])
    if file is not None:
        temp_dir = tempfile.TemporaryDirectory()
        temp_path = os.path.join(temp_dir.name, secure_filename(file.name))
        with open(temp_path, 'wb') as f:
            f.write(file.getbuffer())

        # Load 
        cap = cv2.VideoCapture(temp_path)
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        # VideoWriter
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out_pth = os.path.join(temp_dir.name, 'output.mp4')
        out = cv2.VideoWriter(out_pth, fourcc, fps, frame_size)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # tensor = torch.from_numpy(frame).to(device='cuda')
            res = model.predict(source=frame)

            # bboxes = res.xyxy[0].cpu().numpy()
            # confs = res.xyxy[0].cpu().numpy()
            # for i in res:
            #     bboxes = i.boxes
            #     masks = i.masks
            #     confs = i.probs
            
            bboxes = res[0].boxes
            # masks = res[0].masks
            # print(masks.data)
            # for bbox, conf in zip(bboxes.xyxy, confs):
            #     if conf > 0.5:
            #         x1, y1, x2, y2 = bbox.astype(np.int32)
            #         cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)
        cap.release()
        out.release()

        st.video(out_pth)
        temp_dir.cleanup()

if __name__ == '__main__':
    app()