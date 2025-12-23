from ultralytics import YOLO

if __name__ == '__main__':
    data_path = "dataset/data.yaml"

    model = YOLO("yolo8n.pt")

    model.train(data=data_path,
                epochs=55,
                batch=40,
                imgsz=480,
                name="yolo")