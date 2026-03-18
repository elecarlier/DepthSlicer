import logging
import numpy as np
from pathlib import Path
from PIL import Image

from cli import parse_args

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# Étape 1 — Chargement
# ──────────────────────────────────────────────

def load_images(image_path: str, depth_path: str):
    """Charge l'image originale et la carte de profondeur.

    Returns:
        img   : PIL.Image en mode RGBA
        depth : np.ndarray 2D uint8, valeurs 0-255
    """
    img = Image.open(image_path).convert("RGBA")
    depth = Image.open(depth_path).convert("L")  # niveaux de gris 0-255

    if img.size != depth.size:
        logger.warning("Tailles différentes — redimensionnement depth map %s → %s", depth.size, img.size)
        depth = depth.resize(img.size, Image.LANCZOS)

    logger.info("Image chargée    : %s  %s", img.size, img.mode)
    logger.info("Depth map chargée: %s  min=%d  max=%d",
                depth.size, np.array(depth).min(), np.array(depth).max())

    return img, np.array(depth)


# ──────────────────────────────────────────────
# Étape 2 — Tranches
# ──────────────────────────────────────────────

def make_slices(n: int, depth_min: int = 0, depth_max: int = 255) -> list[tuple[int, int]]:
    """Découpe [depth_min, depth_max] en N bandes égales.

    Exemple avec n=5 :
        [(0, 50), (51, 102), (103, 153), (154, 204), (205, 255)]

    Returns:
        Liste de tuples (borne_basse, borne_haute) incluses.
    """
    step = (depth_max - depth_min + 1) / n
    slices = []
    for i in range(n):
        low  = int(depth_min + i * step)
        high = int(depth_min + (i + 1) * step) - 1 if i < n - 1 else depth_max
        slices.append((low, high))
    return slices


# ──────────────────────────────────────────────
# Étape 3 — Masques
# ──────────────────────────────────────────────

def make_mask(depth: np.ndarray, low: int, high: int) -> np.ndarray:
    """Crée un masque 2D uint8 pour les pixels dont la profondeur est dans [low, high].

    Pixels dans la tranche → 255 (visible)
    Pixels hors tranche    →   0 (transparent)
    """
    return ((depth >= low) & (depth <= high)).astype(np.uint8) * 255


# ──────────────────────────────────────────────
# Étape 4 — Découpage
# ──────────────────────────────────────────────

def apply_mask(img: Image.Image, mask: np.ndarray) -> Image.Image:
    """Applique le masque sur l'image RGBA : les pixels hors tranche deviennent transparents.

    Returns:
        Nouvelle PIL.Image RGBA avec le canal alpha remplacé par le masque.
    """
    layer = img.copy()
    layer.putalpha(Image.fromarray(mask))
    return layer


# ──────────────────────────────────────────────
# Étape 5 — Sauvegarde
# ──────────────────────────────────────────────

def save_layers(layers: list, slices: list[tuple[int, int]], output_dir: Path):
    """Sauvegarde chaque couche découpée en PNG (avec transparence).

    Nommage : layer_0_0-50.png, layer_1_51-102.png, ...
    """
    output_dir.mkdir(parents=True, exist_ok=True)
    for i, (layer, (lo, hi)) in enumerate(zip(layers, slices)):
        path = output_dir / f"layer_{i}_{lo}-{hi}.png"
        layer.save(path)
        logger.info("Sauvegardé : %s", path)


def save_masks(masks: list, slices: list[tuple[int, int]], output_dir: Path):
    """Sauvegarde chaque masque en PNG niveaux de gris dans un sous-dossier masks/.

    Nommage : mask_0_0-50.png, mask_1_51-102.png, ...
    """
    masks_dir = output_dir / "masks"
    masks_dir.mkdir(parents=True, exist_ok=True)
    for i, (mask, (lo, hi)) in enumerate(zip(masks, slices)):
        path = masks_dir / f"mask_{i}_{lo}-{hi}.png"
        Image.fromarray(mask).save(path)
        logger.info("Masque sauvegardé : %s", path)


def run(args):
    img, depth = load_images(args.image, args.depth)
    slices = make_slices(args.slices)
    masks = [make_mask(depth, lo, hi) for lo, hi in slices]
    layers = [apply_mask(img, mask) for mask in masks]
    output_dir = args.output_dir or Path(args.image).parent / "output"
    save_layers(layers, slices, output_dir)
    save_masks(masks, slices, output_dir)


def main():
    args = parse_args()
    run(args)


if __name__ == "__main__":
    main()
