import cv2
import streamlit as st
import tempfile
import subprocess
import os

def detect(file):
    cmd = f'yolo task=detect mode=predict model=best.pt source=test_videos/{file.name} hide_labels=True'
    process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
    output, err = process.communicate()

    yolo_output = []
    for i in output.decode('utf-8').split('\n'):
        if 'video' in i:
            yolo_output.append(i)
    cap = cv2.VideoCapture(file.name)

    # Codec and VideoWriter
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
    # out = cv2.VideoWriter('results/output.mp4', fourcc, fps, frame_size)
    tmp = tempfile.NamedTemporaryFile(delete=False)
    out = cv2.VideoWriter(tmp.name, fourcc, fps, frame_size)

    # Overlay output
    cnt = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        if yolo_output and f'video 1/1 ({cnt})/' in yolo_output[0]:
            detections = yolo_output.pop(0)
            for line in detections.split('\n'):
                if line.startswith('video'):
                    continue
                if line:
                    class_name, conf, left, top, right, bottom = line.split()
                    left, top, right, bottom = map(int, [left, top, right, bottom])
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, f'{class_name} {conf}', (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # Write frame
        out.write(frame)
        # st.image(frame, channels='BGR')
    cap.release()
    out.release()

    return tmp

def app():
    file = st.file_uploader('Upload Video')
    if st.button('Detect'):
        with st.spinner('Detecting Potholes.....'):
            if file is not None:
                output_file = detect(file)    
        
            with open(output_file.name, 'rb') as f: 
                b = f.read()
            st.video(b)
        f.close()
        output_file.close()
        os.unlink(output_file.name)

if __name__ == '__main__':
    app()