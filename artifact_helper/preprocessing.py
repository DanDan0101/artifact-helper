from pathlib import Path
from typing import Tuple

import numpy as np

# from matplotlib import pyplot as plt
from tqdm import tqdm

import imageio.v3 as iio

WINDOW_SIZE = (1080, 1620)  # h, w
ARTIFACT_LOC = (106, 1109)  # Top left
ARTIFACT_SIZE = (868, 404)


def n_frames(file_path: Path) -> int:
    metadata = iio.immeta(file_path, plugin="pyav")
    fps = metadata["fps"]
    duration = metadata["DURATION"]
    hours, minutes, seconds = map(float, duration.split(":"))
    seconds += hours * 3600 + minutes * 60
    # Idk why 2 frames are missing, fudge factor results from testing a single video
    # TODO: test more videos to see if the -2 is consistent
    return int(np.rint(seconds * fps) - 2)


def crop_frame(
    frame: np.ndarray,
    loc: Tuple[int, int] = ARTIFACT_LOC,
    size: Tuple[int, int] = ARTIFACT_SIZE,
) -> np.ndarray:
    # Casting to int makes a copy and is therefore slow
    # TODO: Optimize
    return frame[loc[0] : loc[0] + size[0], loc[1] : loc[1] + size[1], :].astype(
        np.float32
    )


def iter_frames(file_path: Path) -> tqdm:
    return tqdm(
        iio.imiter(file_path, plugin="pyav", thread_type="FRAME"),
        total=n_frames(file_path),
        unit="frames",
    )
