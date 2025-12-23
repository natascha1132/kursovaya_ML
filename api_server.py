import os
import cv2
from fastapi import FastAPI, UploadFile, File, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from ultralytics import YOLO

app = FastAPI()

# Папки
UPLOAD_DIR = "results/uploads"
RESULT_DIR = "results/detections"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(RESULT_DIR, exist_ok=True)

app.mount("/output", StaticFiles(directory=RESULT_DIR), name="output")

templates = Jinja2Templates(directory="templates")
model = YOLO("../Kursovaya/runs/detect/yolo10/weights/best.pt")


@app.get("/")
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/predict")
async def predict(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    results = model.predict(source=file_path, save=False)

    res_plotted = results[0].plot()
    result_filename = f"detected_{file.filename}"
    result_path = os.path.join(RESULT_DIR, result_filename)
    cv2.imwrite(result_path, res_plotted)

    labels = [model.names[int(c)] for c in results[0].boxes.cls]
    prediction_text = f"Обнаружено: {', '.join(set(labels))}" if labels else "Патологий не обнаружено"

    return {
        "prediction": prediction_text,
        "image_url": f"/output/{result_filename}"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)