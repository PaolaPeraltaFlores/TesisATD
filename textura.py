from ultralytics import YOLO

model = YOLO('/home/paola/Desktop/TEXTURA/runs/detect/train4/weights/best.pt')
model.predict(
   source='/home/paola/Desktop/TesisATD/TesisATD/recortar2.jpg', save=True,
   conf=0.55
)