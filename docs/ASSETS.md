# Required assets

SATM requires large runtime assets that are intentionally excluded from GitHub. Download the SATM asset package from [Google Drive](https://drive.google.com/drive/folders/16tAUBDzXszNn6L_z--4EGXzv-Ui7eOgi?usp=drive_link).

After downloading, extract the supplied archives directly into the repository root. Do not add an extra top-level directory. The resulting layout must include:

```text
SATM/
  dataset/
    HumanML3D/
    scene_dataset/
      RGB/
  body_models/
    smpl/
    glove/
    t2m/
  save/
    text_image_mdm/
      model000050000.pt
```

The package should provide the following required assets:

| Asset | Required path |
| --- | --- |
| Scene-aware SATM checkpoint | `save/text_image_mdm/model000050000.pt` |
| HumanML3D support data | `dataset/HumanML3D/` |
| Scene images | `dataset/scene_dataset/RGB/<category>/` |
| SMPL model files | `body_models/smpl/` |
| GloVe and T2M support files | `body_models/glove/` and `body_models/t2m/` |

The Google Drive folder must be shared with intended users. These files are excluded from Git because of size and third-party licence constraints. Keep the original directory structure after extraction.

Then run:

```powershell
python scripts/check_setup.py
```

The checker reports missing files before inference starts.