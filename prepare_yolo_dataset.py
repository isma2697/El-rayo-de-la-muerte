import os
import random
import shutil
from pathlib import Path
import yaml
import subprocess

SOURCE_DIR = "dataset"
IMAGE_DIR = SOURCE_DIR
OUT_IMAGES = os.path.join(SOURCE_DIR, "images")
OUT_LABELS = os.path.join(SOURCE_DIR, "labels")
TRAIN_RATIO = 0.8

def preparar_dataset():
    print("Preparando dataset...")

    # Crear carpetas necesarias
    for subdir in ["images/train", "images/val", "labels/train", "labels/val"]:
        os.makedirs(os.path.join(SOURCE_DIR, subdir), exist_ok=True)

    # Obtener todas las imágenes
    all_imgs = sorted([f for f in os.listdir(IMAGE_DIR) if f.endswith(".jpg")])
    random.shuffle(all_imgs)
    split_index = int(len(all_imgs) * TRAIN_RATIO)
    train_imgs = all_imgs[:split_index]
    val_imgs = all_imgs[split_index:]

    def mover(imagenes, tipo):
        for img in imagenes:
            name = Path(img).stem
            txt = f"{name}.txt"

            shutil.move(os.path.join(IMAGE_DIR, img), os.path.join(OUT_IMAGES, tipo, img))
            shutil.move(os.path.join(IMAGE_DIR, txt), os.path.join(OUT_LABELS, tipo, txt))

    mover(train_imgs, "train")
    mover(val_imgs, "val")

    data = {
        "path": "dataset",
        "train": "images/train",
        "val": "images/val",
        "names": {
            0: "abeja",
            1: "mosca",
            2: "spider"
        }
    }

    with open(os.path.join(SOURCE_DIR, "data.yaml"), "w") as f:
        yaml.dump(data, f, default_flow_style=False)

    print("Dataset preparado correctamente.\n")

def entrenar_yolo():
    print("Iniciando entrenamiento YOLOv8...\n")
    comando = [
        "yolo",
        "task=detect",
        "mode=train",
        "model=yolov8n.pt",
        "data=dataset/data.yaml",
        "epochs=15",
        "imgsz=416"

    ]
    subprocess.run(comando)

def dataset_ya_preparado():
    return all(
        os.path.exists(os.path.join(SOURCE_DIR, path))
        for path in [
            "images/train",
            "images/val",
            "labels/train",
            "labels/val",
            "data.yaml"
        ]
    )

if __name__ == "__main__":
    if not dataset_ya_preparado():
        preparar_dataset()
    else:
        print("Dataset ya preparado. Saltando preparación.\n")
    entrenar_yolo()
