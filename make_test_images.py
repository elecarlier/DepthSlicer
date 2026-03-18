"""Génère des images de test pour valider le découpage par profondeur."""
import numpy as np
from PIL import Image
from pathlib import Path

OUT = Path("test_images")
OUT.mkdir(exist_ok=True)

W, H = 512, 256

# ── Image source : dégradé rouge → bleu (gauche → droite) ──
img_arr = np.zeros((H, W, 4), dtype=np.uint8)
for x in range(W):
    r = int(255 * (1 - x / W))
    b = int(255 * (x / W))
    img_arr[:, x] = [r, 0, b, 255]
Image.fromarray(img_arr, "RGBA").save(OUT / "test_image.png")
print("Créé : test_images/test_image.png  (rouge à gauche, bleu à droite)")

# ── Depth map : dégradé noir → blanc (gauche → droite) ──
depth_arr = np.zeros((H, W), dtype=np.uint8)
for x in range(W):
    depth_arr[:, x] = int(255 * x / W)
Image.fromarray(depth_arr, "L").save(OUT / "test_depth.png")
print("Créé : test_images/test_depth.png  (noir=0 à gauche, blanc=255 à droite)")

print("\nDans cette depth map : 0 (noir) = gauche,  255 (blanc) = droite")
print("Si la convention est '0=proche', les tranches basses = partie rouge de l'image.")
