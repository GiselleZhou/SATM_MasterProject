# GitHub release guide

## 1. Review changes

```powershell
git status
git diff
```

Do not commit changes you do not recognise. Inspect any pre-existing edits to `sample/` or `data_loaders/` before staging them.

## 2. Commit code and reproducibility files

```powershell
git add README.md environment.yml environment-windows.yml .gitignore
git add docs scripts
git add sample model diffusion data_loaders utils visualize prepare train eval
git status
git commit -m "Prepare reproducible SATM release"
```

The `.gitignore` excludes local datasets, body models, checkpoints, results, IDE folders, and videos. Do not use `git add .` before reviewing `git status`.

## 3. Create and push an empty GitHub repository

```powershell
git branch -M main
git remote add origin https://github.com/<YOUR-ACCOUNT>/<YOUR-REPOSITORY>.git
git push -u origin main
```

## 4. Publish authorised large assets

Use a GitHub Release, Zenodo, Hugging Face, or institutionally managed storage for assets you are authorised to redistribute. Add final URLs and checksums to `docs/ASSETS.md`.

For HumanML3D and SMPL, link users to official acquisition instructions unless you have written redistribution permission.

## 5. Validate as a new user

```powershell
git clone https://github.com/<YOUR-ACCOUNT>/<YOUR-REPOSITORY>.git satm-clean
cd satm-clean
conda env create -f environment-windows.yml
conda activate satm
python -m spacy download en_core_web_sm
pip install git+https://github.com/openai/CLIP.git
python scripts/check_setup.py
```

Install the documented assets, rerun the checker, then run the main README example. This clean-clone test is the final proof that the release is reproducible.
