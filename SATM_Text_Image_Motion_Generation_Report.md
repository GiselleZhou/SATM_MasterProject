# SATM: Scene-Aware Text-to-Motion Generation

> SATM extends the MDM (Human Motion Diffusion Model, ICLR 2023) framework with scene-image conditioning for 3D human-motion generation.

## 1. Project Overview

### 1.1 Foundation

- **Reference paper:** [Human Motion Diffusion Model](https://arxiv.org/abs/2209.14916) (ICLR 2023)
- **Reference implementation:** [GuyTevet/motion-diffusion-model](https://github.com/GuyTevet/motion-diffusion-model)
- **Task:** text-to-motion generation, where a natural-language description is mapped to a 3D human-motion sequence.
- **Framework:** PyTorch and diffusion models.
- **Motion data:** HumanML3D.

### 1.2 SATM Objective

SATM introduces a scene image as an additional conditioning signal alongside a concise English action description.

```text
Text prompt: "a person walks on a road"  ──┐
                                            ├──> diffusion model ──> 3D motion sequence
Scene image: road.jpg                     ──┘
```

The intended inference input is a text prompt and a compatible scene image. The scene image is provided by the user or selected explicitly from the scene-image collection.

## 2. Model Design

### 2.1 Architecture

1. A frozen CLIP text encoder converts the action description into a text embedding.
2. A frozen CLIP ViT-B/32 image encoder converts the scene image into an image embedding.
3. Separate learned projection layers map both embeddings to the motion-model conditioning space.
4. Text, image, and timestep embeddings are combined before transformer-based diffusion denoising.
5. The reverse diffusion process produces a 3D motion sequence.

### 2.2 Design Choices

| Component | Choice | Rationale |
|---|---|---|
| Image encoder | CLIP ViT-B/32 | CLIP provides a shared semantic space for text and images. |
| Fusion | Element-wise addition after learned projection | Compatible with the original MDM conditioning design. |
| CLIP weights | Frozen | Retains pretrained multimodal representations while limiting training cost. |
| Training strategy | Fine-tuning from pretrained MDM | Reuses a learned human-motion manifold. |
| Conditional dropout | Independent masking of text and image conditions (`p=0.1`) | Supports classifier-free guidance. |

### 2.3 Scene-Image Condition

SATM adds the `text_image` conditional mode. During inference, the generation script accepts a specific scene image with `--scene_image`. A scene category can also be used to select an image from the local scene collection, but experiments should use a fixed image for reproducibility.

## 3. Repository Structure

```text
SATM/
├── model/                 # Diffusion model and classifier-free guidance
├── diffusion/             # Forward and reverse diffusion processes
├── data_loaders/          # HumanML3D and scene-image loading utilities
├── train/                 # Fine-tuning entry point and training loop
├── sample/                # Motion generation entry point
├── eval/                  # HumanML3D evaluation scripts
├── utils/                 # Parsers, configuration, and model utilities
├── visualize/             # Motion visualisation utilities
├── dataset/               # HumanML3D and scene-image assets (not tracked by Git)
├── save/                  # Checkpoints and evaluation logs (not tracked by Git)
├── body_models/           # SMPL and evaluator assets (not tracked by Git)
├── scripts/               # Reproducibility and inference helpers
└── docs/                  # Asset and release documentation
```

## 4. Data Assets

### 4.1 HumanML3D

HumanML3D provides motion representations, text annotations, normalisation statistics, and train/validation/test splits. The expected local directory is `dataset/HumanML3D/`.

### 4.2 Scene Images

The scene collection is stored under `dataset/scene_dataset/RGB/`. It contains 27 scene/action-oriented categories and 976 RGB images. For controlled qualitative experiments, a specific image is supplied to SATM rather than sampling a category at random.

## 5. Fine-tuning Configuration

SATM was fine-tuned from the pretrained MDM checkpoint using the following main configuration.

| Parameter | Value |
|---|---:|
| Dataset | `humanml` |
| Conditional mode | `text_image` |
| Initial checkpoint | `save/humanml_trans_enc_512/model000200000.pt` |
| Learning rate | `1e-5` |
| Batch size | `128` |
| Fine-tuning steps | `50,000` |
| Final checkpoint | `save/text_image_mdm/model000050000.pt` |

The recorded training run took approximately 31 hours. The training loss decreased from approximately 0.0653 at step 1,000 to approximately 0.0610 at step 50,000.

## 6. Inference

A reproducible scene-aware generation command is:

```powershell
python -m sample.generate `
  --model_path "save/text_image_mdm/model000050000.pt" `
  --text_prompt "a person chops vegetables" `
  --scene_image ".\dataset\scene_dataset\RGB\kitchen\<IMAGE_FILE>" `
  --output_dir ".\outputs\kitchen_chop" `
  --motion_length 3.0 `
  --num_repetitions 1 `
  --guidance_param 2.5 `
  --device 0
```

The preferred public interface is the wrapper script documented in `README.md`. It produces one single-sample video and copies the scene image used into the output directory.

## 7. Evaluation

### 7.1 Metrics

The HumanML3D evaluator reports the following common text-to-motion metrics:

| Metric | Preferred direction | Interpretation |
|---|---|---|
| Matching Score | Lower | Text-motion embedding distance. |
| R-Precision | Higher | Text retrieval accuracy for a generated motion. |
| FID | Lower | Difference between generated and real motion distributions. |
| Diversity | Higher | Variation among generated motions. |
| Multimodality | Higher | Variation among outputs generated for the same condition. |

### 7.2 Recorded SATM Evaluation

The stored SATM evaluation log contains four replications with the `mm_short` configuration. The reported mean values are:

| Metric | SATM mean |
|---|---:|
| Matching Score | 3.279 |
| R-Precision (top 1) | 0.462 |
| R-Precision (top 2) | 0.661 |
| R-Precision (top 3) | 0.763 |
| FID | 0.460 |
| Diversity | 10.074 |
| Multimodality | 2.621 |

These values are traceable to `save/text_image_mdm/eval_humanml_text_image_mdm_000050000_gscale2.5_mm_short.log`.

### 7.3 Qualitative Ablation Material

A controlled qualitative comparison should use the same prompt, seed, motion length, and guidance value for both systems. The only changed condition is the addition of a fixed scene image for SATM. Such a comparison demonstrates visual behaviour; it should not be presented as a statistical significance test.

## 8. Limitations

- Scene compatibility is not guaranteed by the model; users should provide a semantically appropriate scene image.
- A visual comparison alone does not prove a quantitative advantage.
- Claims of improvement over a baseline require matched settings, a shared evaluator, and clearly documented experimental controls.
- Third-party software, pretrained models, datasets, body models, and images must be cited and used according to their respective licences.

## 9. Provenance

SATM is based on the MDM codebase. The repository retains the original MDM licence and documents its dependency and asset requirements in `README.md`, `docs/ASSETS.md`, and `docs/GITHUB_RELEASE.md`.
