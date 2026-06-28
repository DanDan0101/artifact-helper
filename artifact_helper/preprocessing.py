"""
Utilities for preprocessing video files.
Constants are hardcoded for my specific resolution of 1620x1080 @ 30 fps.
"""

import functools
from pathlib import Path
from typing import Literal

import imageio.v3 as iio
import numpy as np
from scipy.signal import find_peaks
from tqdm import tqdm

WINDOW_SIZE = (1080, 1620)  # h, w
ARTIFACT_LOC = (106, 1109)  # Top left
ARTIFACT_SIZE = (868, 404)


@functools.cache
def n_frames(file_path: Path) -> int:
    """
    Counts the total number of frames in a video.

    For some reason, the .mkv containers are missing the metadata for total frames.
    For some even more bizarre reason, calculating total frames from duration and fps metadata
    results in different total frames than the count from iterating through all frames.
    This direct method is acceptably fast for 1620x1080 @ 30 fps.

    Args:
        file_path (Path): Path to video file.

    Returns:
        int: Total number of frames in the video.
    """

    frames = 0
    for _ in iio.imiter(file_path, plugin="pyav", thread_type="FRAME"):
        frames += 1

    return frames


def crop_frame(
    frame: np.ndarray,
    loc: tuple[int, int] = ARTIFACT_LOC,
    size: tuple[int, int] = ARTIFACT_SIZE,
) -> np.ndarray:
    """
    Crops a video frame to the artifact card.

    Args:
        frame (np.ndarray): Uncropped video frame.
        loc (tuple[int, int], optional): Top left corner of artifact card (h, w). Defaults to ARTIFACT_LOC.
        size (tuple[int, int], optional): Size of the artifact card (h, w). Defaults to ARTIFACT_SIZE.

    Returns:
        np.ndarray: Cropped video frame, with size ARTIFACT_SIZE.
    """
    assert frame.shape == (
        WINDOW_SIZE[0],
        WINDOW_SIZE[1],
        3,
    ), f"Expected {WINDOW_SIZE[1]}x{WINDOW_SIZE[0]} resolution, but got {frame.shape[1]}x{frame.shape[0]}"

    cropped_frame = frame[loc[0] : loc[0] + size[0], loc[1] : loc[1] + size[1], :]

    return cropped_frame


def read_cropped_frame(
    file_path: Path,
    index: int,
    loc: tuple[int, int] = ARTIFACT_LOC,
    size: tuple[int, int] = ARTIFACT_SIZE,
    thread_type: Literal["SLICE", "FRAME"] = "SLICE",
) -> np.ndarray:
    """
    Reads the artifact card from a specific frame in a video.

    Args:
        file_path (Path): Path to video file.
        index (int): Index of frame to read.
        loc (tuple[int, int], optional): Top left corner of artifact card (h, w). Defaults to ARTIFACT_LOC.
        size (tuple[int, int], optional): Size of the artifact card (h, w). Defaults to ARTIFACT_SIZE.

    Returns:
        np.ndarray: Cropped video frame, with size ARTIFACT_SIZE.
    """
    return crop_frame(
        iio.imread(file_path, plugin="pyav", index=index),
        loc=loc,
        size=size,
    )


def find_keyframes(
    file_path: Path, distance: int = 3, prominence: int = 5
) -> np.ndarray:
    """
    Finds the keyframes in a video corresponding to unique artifacts.

    Works by calculating the RMS difference between adjacent frames,
    then sorting peaks by distance and prominence.
    Default parameters work well for 1620x1080 @ 30 fps.

    Args:
        file_path (Path): Path to video file.
        distance (int, optional): Minimum distance between peaks. Defaults to 3.
        prominence (int, optional): Minimum prominence of peaks. Defaults to 5.

    Returns:
        np.ndarray: Indices of keyframes in the video.
    """

    prev_frame = read_cropped_frame(file_path, index=0).astype(np.float32)
    diffs = np.empty(n_frames(file_path), dtype=np.float32)

    for i, frame in enumerate(
        tqdm(
            iio.imiter(file_path, plugin="pyav", thread_type="FRAME"),
            total=n_frames(file_path),
            desc="Finding keyframes",
            unit="frames",
            unit_scale=True,
        )
    ):
        curr_frame = crop_frame(frame).astype(np.float32)
        diff = np.sqrt(np.mean((curr_frame - prev_frame) ** 2))  # RMS
        diffs[i] = diff
        prev_frame = curr_frame

    diffs = np.array(diffs)
    peaks = find_peaks(diffs, distance=distance, prominence=prominence)[0]

    centered_peaks = np.insert(
        peaks, 0, 0
    )  # First frame has 0 diff, but is a unique artifact
    dt = np.zeros_like(centered_peaks)
    dt[:-1] = np.diff(centered_peaks) // 2
    dt[-1] = int(np.median(dt[:-1]))

    centered_peaks += dt  # Choose central frame between artifact changes

    return centered_peaks
