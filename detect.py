import os
from ultralytics import YOLO
import cv2


def run_detection(model_path, source_image, save_dir='results/detections'):
    model = YOLO(model_path)
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    results = model.predict(source=source_image, save=True, project=save_dir, name='exp', exist_ok=True)

    print(f"Детекция завершена. Результаты сохранены в: {save_dir}")

    for result in results:
        boxes = result.boxes
        print(f"Найдено патологий: {len(boxes)}")


if __name__ == "__main__":
    MODEL_PATH ="runs/detect/yolo10/weights/best.pt"

    SOURCE = 'dataset/test/images'

    run_detection(MODEL_PATH, SOURCE)