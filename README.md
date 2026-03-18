# DepthSlicer

Découpe une image en couches selon sa carte de profondeur (depth map).

## Principe

À partir d'une image et de sa depth map (image en niveaux de gris), DepthSlicer :

1. Divise la plage de profondeur [0–255] en **N tranches égales**
2. Génère un **masque** par tranche (blanc = dans la tranche, noir = hors tranche)
3. **Découpe** l'image originale selon chaque masque (canal alpha)
4. Sauvegarde les couches et les masques

```
image.png + depth.png  →  layer_0_0-50.png
                           layer_1_51-102.png
                           layer_2_103-153.png
                           ...
                           masks/mask_0_0-50.png
                           masks/mask_1_51-102.png
                           ...
                           recap.png  (avec --recap)
```

## Installation

```bash
pip install Pillow numpy
```

## Utilisation

```bash
python3 main.py -i photo.png -d depth.png -s 5
```

| Argument | Description | Défaut |
|----------|-------------|--------|
| `-i` / `--image` | Image source | requis |
| `-d` / `--depth` | Carte de profondeur (niveaux de gris) | requis |
| `-m` / `--mode` | `1` tranches exclusives (0-20, 20-40…) · `2` cumulatives (0-20, 0-40…) | `1` |
| `-s` / `--slices` | Nombre de tranches | `5` |
| `-o` / `--output_dir` | Dossier de sortie | `<dossier image>/output/` |
| `--recap` | Génère `recap.png` (toutes les tranches côte à côte) | désactivé |

## Structure du projet

```
DepthSlicer/
├── main.py              # logique principale (5 étapes)
├── cli.py               # arguments ligne de commande
└── make_test_images.py  # génère des images synthétiques pour tester
```

## Test rapide

```bash
python3 make_test_images.py                                              # génère test_images/
python3 main.py -i test_images/test_image.png -d test_images/test_depth.png -s 5 --recap
```
