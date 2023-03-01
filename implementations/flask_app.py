import os
from flask import Flask, request, redirect, Response, render_template, url_for, flash
from werkzeug.utils import secure_filename
import torch
import cv2
import tempfile
import subprocess
from ultralytics import YOLO
import numpy as np

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = '/upload_files'
app.config['OUTPUT_FOLDER'] = '/res'
model_path = 'best.pt'
# model = torch.hub.load('ultralytics/yolov5', 'custom', path=model_path)
model = YOLO(model_path)
# Video Extensions
ALLOWED_EXTENSIONS = ['mp4', 'avi', 'mov']

def allowed_file(file):
    return '.' in file and file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# def detect(input_pth, output_pth):
#     cap = cv2.VideoCapture(input_pth)
#     fps = int(cap.get(cv2.CAP_PROP_FPS))
#     frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

#     # VideoWriter
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     tmp = tempfile.NamedTemporaryFile(delete=False)
#     output_pth = tmp.name

#     out = cv2.VideoWriter(output_pth, fourcc, fps, frame_size)
#     while True:
#         ret, frame = cap.read()
#         if ret:
#             break

#         tensor = torch.from_numpy(frame).to(device='cuda')
#         res = model(tensor, size=640)
        
#         # Bounding Boxes and class prob 
#         bboxes = res.xyxy[0].cpu().numpy()
#         confs = res.xyxy[0].cpu().numpy()

#         for bbox, conf in zip(bboxes, confs):
#             if conf > 0.5:
#                 x1, y1, x2, y2 = bbox.astype(np.int32)
#                 cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

#         out.write(frame)
#     cap.release()
#     out.release()
    
#     return output_pth

@app.route('/', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No File')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('No Selected File')
            return redirect(request.url)
        # Upload folder check
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Process video
            cap = cv2.VideoCapture(file_path)
            fps = cap.get(cv2.CAP_PROP_FPS)
            frame_size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out_file_path = os.path.join(app.config['OUTPUT_FOLDER'], 'output.mp4')
            out = cv2.VideoWriter(out_file_path, fourcc, fps, frame_size)

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                tensor = torch.from_numpy(frame).to(device='cuda')
                res = model.predict(tensor)
                
                # Bounding Boxes and class prob 
                bboxes = res.xyxy[0].cpu().numpy()
                confs = res.xyxy[0].cpu().numpy()

                for bbox, conf in zip(bboxes, confs):
                    if conf > 0.5:
                        x1, y1, x2, y2 = bbox.astype(np.int32)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 0, 255), 2)

                out.write(frame)
            cap.release()
            out.release()
            return render_template('output.html', video_file=out_file_path)
    return '''
        <!doctype html>
        <html>
            <head>
                <title>Upload video</title>
            </head>
            <body>
                <h1>Upload a video</h1>
                <form method="post" enctype="multipart/form-data">
                    <input type="file" name="file">
                    <input type="submit" value="Upload">
                </form>
            </body>
        </html>
    '''

if __name__ == '__main__':
    app.run()