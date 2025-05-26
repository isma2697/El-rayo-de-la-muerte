import os
import random
import cv2
import numpy as np
from PIL import Image
from dotenv import load_dotenv

# Cargar configuración
load_dotenv()
NUM_CLASES = int(os.getenv("num_clases"))
WIDTH = int(os.getenv("max_width"))
HEIGHT = int(os.getenv("max_height"))
IMG_LIMITE = os.getenv("img_limite")
IMG_CLASES = eval(os.getenv("img_clases"))
NUM_IMGS = int(os.getenv("num_imagenes"))
MAX_OBJ = int(os.getenv("max_objetos"))
MIN_OBJ = int(os.getenv("min_objetos"))

IMG_DIR = "img"
OUT_DIR = "dataset"
os.makedirs(OUT_DIR, exist_ok=True)

# Cargar imágenes
limite = Image.open(os.path.join(IMG_DIR, IMG_LIMITE)).convert("RGBA") if IMG_LIMITE else None
clases = {
    i: [Image.open(os.path.join(IMG_DIR, f)).convert("RGBA") for f in os.listdir(IMG_DIR) if f.startswith(nombre.split(".")[0])]
    for i, nombre in enumerate(IMG_CLASES)
}

def colocar_limites(img):
    if IMG_LIMITE:
        w, h = limite.size
        img.paste(limite, (0, 0), limite)
        img.paste(limite, (WIDTH - w, 0), limite)
        img.paste(limite, (0, HEIGHT - h), limite)
        img.paste(limite, (WIDTH - w, HEIGHT - h), limite)


def generar_bbox(x, y, w, h):
    x_center = (x + w / 2) / WIDTH
    y_center = (y + h / 2) / HEIGHT
    return x_center, y_center, w / WIDTH, h / HEIGHT

for i in range(1, NUM_IMGS + 1):
    fondo = Image.new("RGBA", (WIDTH, HEIGHT), (255, 255, 255, 255))
    colocar_limites(fondo)

    num_objs = random.randint(MIN_OBJ, MAX_OBJ)
    etiquetas = []

    # Calcular tamaño de celda según número de objetos
    grid_cols = int(MAX_OBJ**0.5)
    grid_rows = int(MAX_OBJ**0.5)
    cell_w = WIDTH // grid_cols
    cell_h = HEIGHT // grid_rows

    celdas = [(x * cell_w, y * cell_h) for x in range(grid_cols) for y in range(grid_rows)]
    random.shuffle(celdas)

    for _ in range(num_objs):
        if not celdas:
            break  # sin celdas disponibles

        clase_id = random.randint(0, NUM_CLASES - 1)
        img_obj = random.choice(clases[clase_id])

        angle = random.randint(0, 360)
        max_scale_w = cell_w / img_obj.width
        max_scale_h = cell_h / img_obj.height
        max_scale = min(max_scale_w, max_scale_h, 1.0)

        if max_scale < 0.5:
            continue

        scale = random.uniform(0.5, max_scale)
        obj = img_obj.resize((int(img_obj.width * scale), int(img_obj.height * scale)))
        obj = obj.rotate(angle, expand=True)

        x_cell, y_cell = celdas.pop()
        x = x_cell + random.randint(0, max(cell_w - obj.width, 1))
        y = y_cell + random.randint(0, max(cell_h - obj.height, 1))

        fondo.paste(obj, (x, y), obj)

        bbox = generar_bbox(x, y, obj.width, obj.height)
        etiquetas.append(f"{clase_id} {' '.join(map(str, bbox))}")

    fondo.convert("RGB").save(f"{OUT_DIR}/img{i}.jpg")
    with open(f"{OUT_DIR}/img{i}.txt", "w") as f:
        f.write("\n".join(etiquetas))

print(f"Generadas {NUM_IMGS} imágenes en la carpeta '{OUT_DIR}'")
