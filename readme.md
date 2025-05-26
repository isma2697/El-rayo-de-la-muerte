# Proyecto "El Rayo de la Muerte"

## Descripción

Sistema de localización y seguimiento automático de insectos (abejas, moscas y arañas) sobre imágenes generadas sintéticamente. Cuando se detecta una araña, se simula un puntero láser apuntando al centro.

## Estructura del repositorio

```
rayo/
├── .env
├── generate_dataset.py
├── prepare_yolo_dataset.py
├── run_entrenamiento.py
├── simulador_laser.py
├── img/
│   ├── abeja.png
│   ├── abeja1.png
│   ├── abeja2.png
│   ├── mosca.png
│   ├── mosca1.png
│   ├── mosca2.png
│   ├── spider.png
│   ├── spider1.png
│   ├── spider2.png
│   └── laser.png
├── dataset/
│   ├── images/
│   │   ├── train/...
│   │   └── val/...
│   ├── labels/
│   │   ├── train/...
│   │   └── val/...
│   └── data.yaml
└── runs/
    └── detect/
        └── train/weights/best.pt
```

## 1. Configuración del entorno

1. Clona o descarga el repositorio.
2. Crea y activa entorno virtual:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
3. Instala dependencias:

   ```bash
   pip install python-dotenv Pillow opencv-python ultralytics pyyaml
   ```

## 2. Archivo `.env`

Define variables para la generación del dataset:

```env
num_clases=3
max_width=640
max_height=480
img_limite=
img_clases=["abeja.png","mosca.png","spider.png"]
num_imagenes=1000
max_objetos=20
min_objetos=10
```

## 3. Generación del dataset

Ejecuta:

```bash
python3 generate_dataset.py
```

* Genera 1000 imágenes con objetos no superpuestos.
* Guarda `imgX.jpg` y `imgX.txt` con etiquetas en YOLO.

## 4. Preparar para YOLO

Ejecuta:

```bash
python3 prepare_yolo_dataset.py
```

* Crea split 80/20 en `dataset/images` y `dataset/labels`.
* Genera `dataset/data.yaml` con las clases.

## 5. Entrenamiento del modelo

Entrena YOLOv8:

```bash
python3 run_entrenamiento.py
```

* Ajusta automáticamente split y `data.yaml`.
* Parámetros: `model=yolov8n.pt`, `epochs=15`, `imgsz=416`.
* Salida: `runs/detect/train/weights/best.pt`.

## 6. Simulación de puntero láser

Ejecuta:

```bash
python3 simulador_laser.py
```

* Carga `best.pt`, detecta arañas y superpone `laser.png` sobre cada araña.
* Muestra ventana Tkinter con resultado.

## Guion para presentación

1. **Introducción**: objetivo y motivación.
2. **Generación de datos**: explicar `generate_dataset.py`, configuraciones, impresiones de imágenes.
3. **Preparar YOLO**: estructura de carpetas y `data.yaml`.
4. **Entrenamiento**: comandos, resultados de métricas (`mAP50 ≈0.995`).
5. **Simulación**: demo en vivo del simulador, mostrando láser sobre arañas, explicar código de `simulador_laser.py`.
6. **Conclusiones**: desempeño, posibles mejoras (dinámica, control de servos reales).

---

**Fin del README**
