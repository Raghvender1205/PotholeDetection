from fastapi import FastAPI, File, UploadFile, Path
import cv2
import numpy as np
import os
import subprocess
import tempfile
from starlette.responses import StreamingResponse

app = FastAPI()

# Upload File
@app.route('/', methods=['POST', 'GET'])
async def create_file(file: UploadFile = File(...)):
    with tempfile.NamedTemporaryFile(delete=False) as tmp:
        # Write the contents of the uploaded file to a temporary file
        contents = await file.read()
        tmp.write(contents)
        tmp.flush()
        file_path = tmp.name
    )

    result = subprocess.run(['yolo', "task=detect", "mode=predict", "model=best.pt", f"source={file_path}", "hide_labels=False", "save=True"], capture_output=True)
    return {"filename": file.filename, "file_path": file_path, "output": result.stdout.decode()}
