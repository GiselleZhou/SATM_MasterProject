import os
import random
import torch
from PIL import Image


class SceneImageLoader:
    def __init__(self, scene_dir, clip_preprocess):
        self.scene_dir = scene_dir
        self.preprocess = clip_preprocess
        self.image_paths = []
        for root, _, files in os.walk(scene_dir):
            for f in files:
                if f.lower().endswith(('.png', '.jpg', '.jpeg')):
                    self.image_paths.append(os.path.join(root, f))
        print(f'SceneImageLoader: found {len(self.image_paths)} images in {scene_dir}')

    def sample(self, n):
        """Return n random scene images as preprocessed tensor [n, 3, 224, 224]."""
        chosen = random.choices(self.image_paths, k=n) if n <= len(self.image_paths) else [
            random.choice(self.image_paths) for _ in range(n)
        ]
        images = []
        for path in chosen:
            img = Image.open(path).convert('RGB')
            images.append(self.preprocess(img))
        return torch.stack(images, dim=0)
