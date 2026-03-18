
import logging
from pathlib import Path
from PIL import Image

from cli import parse_args

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)

 
# ──────────────────────────────────────────────
# Chargement
# ──────────────────────────────────────────────
 
def load_images(image_path: str, depth_path: str):
    """Charge l'image originale et la carte de profondeur."""
    img = Image.open(image_path).convert("RGBA")
    depth = Image.open(depth_path).convert("L")  # niveaux de gris 0-255
 
    # if img.size != depth.size:
    #     print(f"[!] Redimensionnement de la depth map {depth.size} → {img.size}")
    #     depth = depth.resize(img.size, Image.LANCZOS)
 
    return img, np.array(depth)
 


def run(args):
    pass

def main():
    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()
