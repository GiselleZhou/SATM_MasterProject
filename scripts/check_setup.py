"""Check that the local assets required for SATM scene-aware inference exist."""

from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = {
    "scene-aware checkpoint": ROOT / "save" / "text_image_mdm" / "model000050000.pt",
    "HumanML3D directory": ROOT / "dataset" / "HumanML3D",
    "scene-image directory": ROOT / "dataset" / "scene_dataset" / "RGB",
    "SMPL directory": ROOT / "body_models" / "smpl",
    "GloVe directory": ROOT / "body_models" / "glove",
    "T2M support directory": ROOT / "body_models" / "t2m",
}


def main() -> int:
    missing = [name for name, path in REQUIRED.items() if not path.exists()]
    print(f"Repository root: {ROOT}")
    for name, path in REQUIRED.items():
        status = "OK" if path.exists() else "MISSING"
        print(f"[{status}] {name}: {path.relative_to(ROOT)}")

    if missing:
        print("\nMissing assets: " + ", ".join(missing))
        print("See docs/ASSETS.md for acquisition and placement instructions.")
        return 1

    print("\nAll required inference paths are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
