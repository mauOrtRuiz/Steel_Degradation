# ==============================================================================
# GENERADOR DE PARCHES ROI DESDE D:\Nayte\Dataset_Generated_Nayte_V3
# Coincidencia: Imagen.jpg -> Imagen_class.png (Excluye *_visual.jpg / *_visual.png)
# ==============================================================================
# ==============================================================================
# PIPELINE COMPLETO: EXTRACTOR DE PARCHES CON MÁSCARAS CORREGIDAS A CLASES [0, 1, 2, 3]
# Lee imágenes/máscaras originales e instala parches limpios de 1 canal.
# ==============================================================================
# ==============================================================================
# PIPELINE COMPLETO: EXTRACTOR DE PARCHES CON MÁSCARAS CORREGIDAS A CLASES [0, 1, 2, 3]
# Lee imágenes/máscaras originales e instala parches limpios de 1 canal.
# ==============================================================================
# ==============================================================================
# PIPELINE CORREGIDO: EXTRACCIÓN DE PARCHES DESDE REGIONAL DE CORROSIÓN (_roi)
# Genera Dataset U-Net (256x256) y Dataset Fractal (95% ROI) dividido en subcarpetas.
# ==============================================================================
# ==============================================================================
# PIPELINE CORREGIDO: EXTRACCIÓN DE PARCHES DESDE REGIONAL DE CORROSIÓN (_roi)
# Genera Dataset U-Net (256x256) y Dataset Fractal (95% ROI) dividido en subcarpetas.
# ==============================================================================
import os
import re
import cv2
import numpy as np
import pandas as pd
from pathlib import Path
from tqdm import tqdm

def mapear_a_clases_0123(mask_grayscale: np.ndarray) -> np.ndarray:
    """ Convierte intensidades (0, 85, 170, 255) a enteros [0, 1, 2, 3] """
    clases = np.round(mask_grayscale.astype(np.float32) / 85.0).astype(np.uint8)
    return np.clip(clases, 0, 3)

def obtener_categoria_tiempo(nombre_carpeta: str) -> str:
    """ Extrae etiquetas como '0h', '500h', '1000h', '1500h' desde nombres como '1000 T0' """
    match = re.search(r'(\d+)', nombre_carpeta)
    if match:
        horas = match.group(1)
        return f"{horas}h"
    return nombre_carpeta.strip()

def extraer_dataset_parches_nayte_final(
    base_dir: str = r'D:\Nayte\Dataset_Generated_Nayte_V3',
    output_unet_dir: str = r'D:\Nayte\Dataset_Parches_256',
    output_fractal_dir: str = r'D:\Nayte\Dataset_Fractal_95',
    patch_size: int = 256,
    stride: int = 128,
    min_roi_unet: float = 0.40,
    min_roi_fractal: float = 0.95,
    samples_per_group_fractal: int = 30
):
    base_path = Path(base_dir)

    # 1. Preparar salida U-Net
    out_img_unet = Path(output_unet_dir) / 'images'
    out_roi_unet = Path(output_unet_dir) / 'masks'
    out_img_unet.mkdir(parents=True, exist_ok=True)
    out_roi_unet.mkdir(parents=True, exist_ok=True)

    # 2. Buscar JPGs primarios (excluyendo _class, _visual, _roi)
    todas_las_imagenes = [
        f for f in base_path.rglob('*.jpg') 
        if not any(suffix in f.stem.lower() for suffix in ['_class', '_visual', '_roi'])
    ]

    print(f"📦 Encontradas {len(todas_las_imagenes)} imágenes JPG principales.")

    patch_records_unet = []
    fractal_candidates_by_group = {}

    for img_path in tqdm(todas_las_imagenes, desc="Procesando imágenes"):
        # Localizar máscara de clases (_class.png)
        mask_class_path = img_path.parent / f"{img_path.stem}_class.png"
        if not mask_class_path.exists():
            posibles = list(img_path.parent.glob(f"{img_path.stem}_class.[pP][nN][gG]"))
            if posibles:
                mask_class_path = posibles[0]
            else:
                continue

        # Localizar máscara de región ROI (_roi.png o _roi.jpg)
        roi_region_path = img_path.parent / f"{img_path.stem}_roi.png"
        if not roi_region_path.exists():
            posibles_roi = list(img_path.parent.glob(f"{img_path.stem}_roi.[pP][jJ][nN][gG]*"))
            if posibles_roi:
                roi_region_path = posibles_roi[0]
            else:
                # Si no existe archivo _roi específico, se usa la clase para evaluar región
                roi_region_path = mask_class_path

        # Cargar archivos
        img = cv2.imread(str(img_path), cv2.IMREAD_COLOR)
        mask_class_gray = cv2.imread(str(mask_class_path), cv2.IMREAD_GRAYSCALE)
        roi_region_gray = cv2.imread(str(roi_region_path), cv2.IMREAD_GRAYSCALE)

        if img is None or mask_class_gray is None or roi_region_gray is None:
            continue

        # Mapear clases a enteros [0, 1, 2, 3]
        mask_clases = mapear_a_clases_0123(mask_class_gray)

        # Región binaria para calcular el porcentaje (>0 es región válida/interés)
        region_binaria = (roi_region_gray > 0).astype(np.uint8)

        h, w = mask_clases.shape[:2]
        cat_tiempo = obtener_categoria_tiempo(img_path.parent.name)
        base_name = img_path.stem
        patch_id = 0

        if cat_tiempo not in fractal_candidates_by_group:
            fractal_candidates_by_group[cat_tiempo] = []

        # Ventana deslizante
        for y in range(0, h - patch_size + 1, stride):
            for x in range(0, w - patch_size + 1, stride):
                region_patch = region_binaria[y:y + patch_size, x:x + patch_size]
                coverage = np.sum(region_patch) / (patch_size * patch_size)

                # Criterio Dataset U-Net (>= 40% ROI)
                if coverage >= min_roi_unet:
                    img_patch = img[y:y + patch_size, x:x + patch_size]
                    mask_patch = mask_clases[y:y + patch_size, x:x + patch_size]

                    filename = f"{cat_tiempo}_{base_name}_p{patch_id:04d}_y{y}_x{x}.png"

                    path_img_u = out_img_unet / filename
                    path_roi_u = out_roi_unet / filename

                    cv2.imwrite(str(path_img_u), img_patch)
                    cv2.imwrite(str(path_roi_u), mask_patch)

                    patch_records_unet.append({
                        'patch_filename': filename,
                        'categoria_tiempo': cat_tiempo,
                        'origen_img': img_path.name,
                        'pos_y': y,
                        'pos_x': x,
                        'roi_coverage': round(float(coverage), 4),
                        'img_path': str(path_img_u),
                        'mask_path': str(path_roi_u)
                    })

                    # Criterio Candidato Fractal (>= 95% ROI)
                    if coverage >= min_roi_fractal:
                        fractal_candidates_by_group[cat_tiempo].append({
                            'filename': filename,
                            'categoria_tiempo': cat_tiempo,
                            'roi_coverage': round(float(coverage), 4),
                            'img_patch': img_patch,
                            'mask_patch': mask_patch
                        })

                    patch_id += 1

    # Guardar Manifiesto U-Net
    df_unet = pd.DataFrame(patch_records_unet)
    df_unet.to_csv(Path(output_unet_dir) / 'manifest_parches.csv', index=False)

    # 3. Guardar Dataset Fractal dividido por carpetas (0h, 500h, 1000h, 1500h)
    records_fractal_final = []
    np.random.seed(42)

    for cat_tiempo, candidates in fractal_candidates_by_group.items():
        if not candidates:
            continue

        # Crear subcarpetas para esta categoría
        group_img_dir = Path(output_fractal_dir) / cat_tiempo / 'images'
        group_roi_dir = Path(output_fractal_dir) / cat_tiempo / 'masks'
        group_img_dir.mkdir(parents=True, exist_ok=True)
        group_roi_dir.mkdir(parents=True, exist_ok=True)

        n_select = min(len(candidates), samples_per_group_fractal)
        selected = np.random.choice(candidates, size=n_select, replace=False)

        for item in selected:
            fname = f"FRACTAL_{item['filename']}"
            p_img = group_img_dir / fname
            p_roi = group_roi_dir / fname

            cv2.imwrite(str(p_img), item['img_patch'])
            cv2.imwrite(str(p_roi), item['mask_patch'])

            records_fractal_final.append({
                'patch_filename': fname,
                'categoria_tiempo': cat_tiempo,
                'roi_coverage': item['roi_coverage'],
                'img_path': str(p_img),
                'mask_path': str(p_roi)
            })

    df_fractal = pd.DataFrame(records_fractal_final)
    df_fractal.to_csv(Path(output_fractal_dir) / 'manifest_fractal.csv', index=False)

    print(f"\n✅ Extracción finalizada con éxito.")
    print(f"🧩 Parches Totales U-Net (>=40% ROI): {len(df_unet)}")
    print(f"🔬 Parches Totales Fractales (>=95% ROI): {len(df_fractal)}")

    return df_unet, df_fractal

# ==============================================================================
# EJECUCIÓN DIRECTA
# ==============================================================================
df_unet, df_fractal = extraer_dataset_parches_nayte_final(
    base_dir=r'D:\Nayte\Dataset_Generated_Nayte_V3',
    output_unet_dir=r'D:\Nayte\Dataset_Parches_256',
    output_fractal_dir=r'D:\Nayte\Dataset_Fractal_95',
    patch_size=256,
    stride=128,
    min_roi_unet=0.40,
    min_roi_fractal=0.95,
    samples_per_group_fractal=30
)