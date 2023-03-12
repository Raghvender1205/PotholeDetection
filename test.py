import gradio as gr
import cv2
from ultralytics import YOLO

model = YOLO('best.pt')

def show_preds(video_path, output_path):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)
    fourcc = cv2.VideoWriter_fourcc(*'h264')
    writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    while True:
        ret, frame = cap.read()
        if ret:
            frame_copy = frame.copy()
            outputs = model.predict(source=frame)
            res = outputs[0].cpu().numpy()
            for i, det in enumerate(res.boxes.xyxy):
                cv2.rectangle(
                    frame_copy, 
                    (int(det[0]), int(det[1])),
                    (int(det[2]), int(det[3])),
                    color=(0, 0, 255),
                    thickness=2,
                    lineType=cv2.LINE_AA
                )
            writer.write(frame_copy)
            yield cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)
        else:
            break
    writer.release()

input_video = [
    gr.inputs.Video(type='file', label='Input Video'),
]
output_video = [
    gr.outputs.Video(type='file', label='Output Video'),
]

interface = gr.Interface(
    show_preds,
    inputs=input_video, # type: ignore
    outputs=output_video, # type: ignore
    title='Pothole Detection',
    description='Potholes Detection using YOLOv8',
)

interface.queue().launch()
