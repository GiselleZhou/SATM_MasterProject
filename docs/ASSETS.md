# Required assets

The following assets are required for scene-aware inference but are not stored in Git. Place them at the exact relative paths shown below.

| Asset | Required path | Acquisition |
| --- | --- | --- |
| Scene-aware SATM checkpoint | `save/text_image_mdm/model000050000.pt` | Download the checkpoint released by this project's maintainer. Add the final authorised URL here before publishing. |
| HumanML3D support data | `dataset/HumanML3D/` | Follow the HumanML3D project's licence and download instructions. Keep its structure unchanged. |
| Scene images | `dataset/scene_dataset/RGB/<category>/` | Obtain the authorised scene-image package released by the maintainer, or use images you have permission to use. |
| SMPL model | `body_models/smpl/` | Register with the official SMPL provider and accept its licence. |
| GloVe / T2M support files | `body_models/glove/` and `body_models/t2m/` | Use upstream MDM preparation instructions or an authorised package. |

Before publishing, replace the checkpoint and scene-package placeholders with stable download URLs and SHA-256 checksums. Do not publish HumanML3D or SMPL assets unless their licences explicitly permit redistribution.

After placing assets, run:

```powershell
python scripts/check_setup.py
```
