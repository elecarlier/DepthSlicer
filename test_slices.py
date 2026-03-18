"""Test visuel — utilise les fonctions de main.py."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw
from main import load_images, make_slices, make_mask, apply_mask, save_layers

OUT = Path("test_images")
n = int(sys.argv[1]) if len(sys.argv) > 1 else 5

img, depth = load_images(OUT / "test_image.png", OUT / "test_depth.png")
slices = make_slices(n=n)
layers = [apply_mask(img, make_mask(depth, lo, hi)) for lo, hi in slices]

# Sauvegarde des couches (avec transparence)
save_layers(layers, slices, OUT)

# ── Image récap : toutes les tranches côte à côte sur fond gris ──
W, H = img.size
LABEL_H = 30
recap = Image.new("RGBA", (W * len(slices), H + LABEL_H), (50, 50, 50, 255))
draw = ImageDraw.Draw(recap)

for i, (layer, (lo, hi)) in enumerate(zip(layers, slices)):
    preview = Image.new("RGBA", (W, H), (220, 220, 220, 255))
    preview.paste(layer, mask=layer.split()[3])
    recap.paste(preview, (i * W, LABEL_H))
    draw.text((i * W + 5, 5), f"T{i}  [{lo}-{hi}]", fill=(255, 255, 200))

recap.save(OUT / "recap_all_slices.png")
print("→ Ouvre test_images/recap_all_slices.png")
