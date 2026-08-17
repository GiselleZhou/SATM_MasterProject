"""Check that the local assets required for SATM scene-aware inference exist."""

from pathlib import Path
import shutil
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

    system_ffmpeg = shutil.which("ffmpeg")
    fallback_ffmpeg = None
    if system_ffmpeg is None:
        try:
            import imageio_ffmpeg
            candidate = Path(imageio_ffmpeg.get_ffmpeg_exe())
            if candidate.is_file():
                fallback_ffmpeg = candidate
        except Exception:
            pass

    encoder = system_ffmpeg or fallback_ffmpeg
    encoder_status = "OK" if encoder else "MISSING"
    print(f"[{encoder_status}] MP4 encoder: {encoder or 'ffmpeg not found'}")
    if encoder is None:
        missing.append("MP4 encoder (ffmpeg or imageio-ffmpeg)")

    if missing:
        print("\nMissing requirements: " + ", ".join(missing))
        print("See docs/ASSETS.md and README.md for setup instructions.")
        return 1

    print("\nAll required inference paths and MP4 rendering support are present.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
