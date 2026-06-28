# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: artifact-helper:default (3.12.8)
#     language: python
#     name: python3
# ---

# %%
from pathlib import Path

import imageio.v3 as iio
import numpy as np
import pytesseract
from matplotlib import pyplot as plt
from tqdm.notebook import tqdm

from artifact_helper.preprocessing import (
    find_keyframes,
    n_frames,
    read_cropped_frame,
)

# %%
media_dir = "media"
file_format = "mkv"
file_name = "artifacts_2026-06-28_00-32-14"

file_path = Path(f"./{media_dir}/{file_name}.{file_format}")
output_dir = Path(f"./{media_dir}/{file_name}")

# %%
for path in Path(f"./{media_dir}").glob("*.mkv"):
    print(f"{path.name[:-len(file_format)-1]} has {n_frames(path)} frames")

# %%
keyframes = find_keyframes(file_path)
print(f"Detected {keyframes.shape[0]} unique artifacts in {file_path.name}.")

# %%
for i, keyframe in enumerate(tqdm(keyframes)):
    frame = read_cropped_frame(file_path, keyframe)
    output_file = output_dir.joinpath(f"{i}.png")
    iio.imwrite(output_file, frame)

# %%
