# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.19.3
#   kernelspec:
#     display_name: default
#     language: python
#     name: python3
# ---

# %%
from pathlib import Path

import imageio.v3 as iio
import numpy as np
from matplotlib import pyplot as plt
from tqdm.notebook import tqdm

from artifact_helper.preprocessing import find_keyframes, n_frames, read_cropped_frame

# %%
media_dir = "media"
file_format = "mkv"
file_name = "artifacts_long"
file_path = Path(f"./{media_dir}/{file_name}.{file_format}")

# %%
for path in Path(f"./{media_dir}").glob("*.mkv"):
    print(f"{path.name[:-len(file_format)-1]} has {n_frames(path)} frames")

# %%
peaks = find_keyframes(file_path)
print(f"Detected {peaks.shape[0]} unique artifacts in {file_name}.")

# %%
test_img = read_cropped_frame(file_path, index=peaks[0])

# %%
