import argparse
from pathlib import Path


def parse_args():
    """Définition des arguments CLI."""
    parser = argparse.ArgumentParser(
        description="Modifications sur images lenticulaires (ajout mire, traits de repérage)."
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
        help="Chemin de la carte de profondeur."
    )
    parser.add_argument(
        "--mode",
        type=int,
        choices=[1, 2],
        default=1,
        help=(
            "Mode 1:"
            "Mode 2:" \
        )
    )
    parser.add_argument(
        "-s", "--slices",
        type=str,
        default=5,
        metavar="N",
        help="Nombre de tranches égales"
    )    
    parser.add_argument(
        "-o", "--output",
        type=str,
        default=None,
        help="Nom du fichier de sortie (sans chemin). Par défaut: <image>_mod.png"
    )
    parser.add_argument(
        "-d", "--output_dir",
        type=Path,
        default=None,
        help="Dossier de sortie. Par défaut: même dossier que l'image d'entrée."
    )
 
    return parser.parse_args()
