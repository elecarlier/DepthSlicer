import argparse
from pathlib import Path


def parse_args():
    """Définition des arguments CLI."""
    parser = argparse.ArgumentParser(
        description="DepthSlicer — découpe une image par tranches de profondeur."
    )

    parser.add_argument(
        "-i", "--image",
        type=Path,
        required=True,
        help="Chemin de l'image source."
    )
    parser.add_argument(
        "-d", "--depth",
        type=Path,
        required=True,
        help="Chemin de la carte de profondeur (image en niveaux de gris)."
    )
    parser.add_argument(
        "-m", "--mode",
        type=int,
        choices=[1, 2],
        default=1,
        help="Mode 1: tranches exclusives (0-20, 20-40, ...). Mode 2: tranches cumulatives (0-20, 0-40, ...)."
    )
    parser.add_argument(
        "-s", "--slices",
        type=int,
        default=5,
        metavar="N",
        help="Nombre de tranches égales (défaut: 5)."
    )
    parser.add_argument(
        "-o", "--output_dir",
        type=Path,
        default=None,
        help="Dossier de sortie. Par défaut: même dossier que l'image d'entrée."
    )
    parser.add_argument(
        "--recap",
        action="store_true",
        help="Génère un récap visuel de toutes les tranches côte à côte (recap.png)."
    )

    return parser.parse_args()
