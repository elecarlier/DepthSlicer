from pathlib import Path

def clean_input_output(folders=None, exts=None):
    """
    Nettoie les fichiers image dans les dossiers spécifiés.

    Args:
        folders (list[str] or list[Path]): liste des dossiers à nettoyer.
            Par défaut ["input", "output"].
        exts (list[str]): extensions de fichiers à supprimer.
            Par défaut [".png", ".jpg", ".jpeg"].
    """
    if folders is None:
        folders = ["input", "output"]
    if exts is None:
        exts = [".png", ".jpg", ".jpeg"]

    for folder in folders:
        folder_path = Path(folder)
        if not folder_path.exists():
            print(f"Dossier introuvable : {folder}")
            continue

        for file_path in folder_path.rglob("*"):
            if file_path.suffix.lower() in exts:
                try:
                    file_path.unlink()
                    print(f"Supprimé : {file_path}")
                except Exception as e:
                    print(f"Erreur suppression {file_path} : {e}")

    print("✅ Nettoyage terminé")


if __name__ == "__main__":
    clean_input_output()
