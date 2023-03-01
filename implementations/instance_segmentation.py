# Yolo Instance Segmentation on an image
from ultralyticsplus import YOLO, render_result

model = YOLO('keremberke/yolov8n-pothole-segmentation')
model.overrides['conf'] = 0.25
model.overrides['iou'] = 0.45  # NMS IoU threshold
model.overrides['agnostic_nms'] = False  # NMS class-agnostic
model.overrides['max_det'] = 1000

img = 'test/test.jpg'
res = model.predict(img)

print(res[0].boxes)
print(res[0].masks)
render = render_result(model=model, image=img, result=res[0])
render.show()