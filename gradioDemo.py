import gradio as gr
import cv2
from ultralytics import YOLO

model = YOLO('best.pt')
# video_path = 'Deployment\\test_videos\\test2.mp4'
def show_preds(video_path):
    cap = cv2.VideoCapture(video_path)
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
            yield cv2.cvtColor(frame_copy, cv2.COLOR_BGR2RGB)

input_video = [
    gr.components.Video(type='filepath', label='Input Video'),
]
outputs_video = [
    gr.components.Image(type='numpy', label='Output Image'),
]
interface_video = gr.Interface(
    fn=show_preds,
    inputs=input_video,
    outputs=outputs_video,
    title='Pothole Detection',
    #examples=video_path,
    cache_examples=False,
)

gr.TabbedInterface(   
    [interface_video],
    tab_names=['Video Inference']
).queue().launch()