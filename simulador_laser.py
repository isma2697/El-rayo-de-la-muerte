import cv2
import numpy as np
from PIL import Image, ImageTk
from ultralytics import YOLO
import tkinter as tk

# Cargar modelo y láser
model = YOLO("runs/detect/train/weights/best.pt")
laser = Image.open("img/laser.png").convert("RGBA").resize((30, 30))

# Cargar imagen base
img_path = "dataset/images/val/img24.jpg"
img_cv = cv2.imread(img_path)
img_pil = Image.fromarray(cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)).convert("RGBA")

# Detección
results = model.predict(source=img_cv, conf=0.5, imgsz=416)[0]

# Colocar láser sobre arañas
for box in results.boxes:
    cls_id = int(box.cls[0])
    if cls_id == 2:  # spider
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2
        lx = cx - laser.width // 2
        ly = cy - laser.height // 2
        img_pil.paste(laser, (lx, ly), laser)

# Crear ventana de Tkinter
root = tk.Tk()
root.title("Arañas con láser")

# Convertir imagen a formato Tkinter
final_img = ImageTk.PhotoImage(img_pil)

label = tk.Label(root, image=final_img)
label.pack()

root.mainloop()
